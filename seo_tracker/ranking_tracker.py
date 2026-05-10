"""SEO Ranking Tracker — track domain position over time.

Three providers (none of them can affect rankings — read-only by design):
  - duckduckgo: free HTML scrape (queries DDG, never Google, never your site)
  - manual:     interactive entry; YOU search Google incognito and type position
  - serper:     Serper.dev API (set SERPER_API_KEY env var; free 2,500 queries/mo)

Append-only history.csv keeps the trend record. Re-runnable any time.

Safety:
  - Script never visits the target site or clicks search results.
  - Cannot inflate or deflate CTR. Cannot affect Google's view of you.
  - Safe to run automated on a schedule.

Usage:
    python ranking_tracker.py check                  # one-shot check (no telegram)
    python ranking_tracker.py check --provider serper
    python ranking_tracker.py weekly                 # check + report + telegram summary
    python ranking_tracker.py weekly --provider serper
    python ranking_tracker.py report                 # regenerate report.html from history
    python ranking_tracker.py list                   # print keyword list
    python ranking_tracker.py add "keyword text"     # add a keyword (interactive)

Designed to be reused for future site builds: edit config.json domain + keywords.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
HISTORY_PATH = ROOT / "history.csv"
REPORT_PATH = ROOT / "report.html"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36"
RANK_NOT_FOUND = -1   # sentinel: domain not in top N
RANK_TOP_N = 50       # how deep we look


# ---------- Config / history I/O ----------

def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save_config(cfg: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def history_writer():
    """Open history.csv in append mode, write header if file is new."""
    new_file = not HISTORY_PATH.exists()
    f = HISTORY_PATH.open("a", newline="", encoding="utf-8")
    w = csv.writer(f)
    if new_file:
        w.writerow(["timestamp_utc", "keyword", "tier", "category", "lang",
                    "provider", "rank", "found_url", "note"])
    return f, w


def write_history_row(w, kw_obj: dict, provider: str, rank: int,
                      found_url: str = "", note: str = "") -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    w.writerow([ts, kw_obj["q"], kw_obj.get("tier", ""), kw_obj.get("category", ""),
                kw_obj.get("lang", ""), provider, rank, found_url, note])


# ---------- Providers ----------

def provider_duckduckgo(query: str, target_domain: str, country: str, lang: str) -> tuple[int, str, str]:
    """Scrape DuckDuckGo HTML SERP. Returns (rank, found_url, note).

    rank = 1-N if found in top N, RANK_NOT_FOUND otherwise.
    """
    kl = f"{country}-{lang}" if country and lang else "wt-wt"
    params = urllib.parse.urlencode({"q": query, "kl": kl})
    url = f"https://html.duckduckgo.com/html/?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as exc:
        return RANK_NOT_FOUND, "", f"ddg-error: {exc.__class__.__name__}"

    # DDG HTML wraps each result link with class result__a (deep link) and result__url (display URL).
    # We want destination URLs in order. They appear as href="//duckduckgo.com/l/?uddg=ENCODED&..." or sometimes plain.
    # Simpler: find all uddg-encoded URLs in order.
    raw_urls: list[str] = []
    for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"', html):
        href = m.group(1)
        # Decode the uddg= redirect parameter if present
        if "uddg=" in href:
            qs = urllib.parse.urlparse(href).query
            decoded = urllib.parse.parse_qs(qs).get("uddg", [""])[0]
            raw_urls.append(decoded or href)
        else:
            raw_urls.append(href)

    target_norm = target_domain.lower().lstrip(".").replace("www.", "")
    for i, raw in enumerate(raw_urls[:RANK_TOP_N], start=1):
        try:
            host = urllib.parse.urlparse(raw).netloc.lower().replace("www.", "")
        except Exception:
            host = raw.lower()
        if host == target_norm or host.endswith("." + target_norm):
            return i, raw, f"ddg-found-pos-{i}"

    if not raw_urls:
        return RANK_NOT_FOUND, "", "ddg-no-results-parsed"
    return RANK_NOT_FOUND, "", f"ddg-checked-{len(raw_urls)}-results"


def provider_manual(query: str, target_domain: str, *_args) -> tuple[int, str, str]:
    print(f"\n  Search Google (incognito, location=Sweden) for:")
    print(f"      {query}")
    print(f"  Find the first result containing {target_domain}.")
    print(f"  Enter the position number (1, 2, 3, ...), or:")
    print(f"      0 = not found in top {RANK_TOP_N}")
    print(f"      s = skip this keyword")
    while True:
        ans = input("  Position: ").strip().lower()
        if ans == "s":
            return RANK_NOT_FOUND, "", "manual-skipped"
        if ans == "0":
            return RANK_NOT_FOUND, "", "manual-not-in-top-50"
        try:
            n = int(ans)
            if 1 <= n <= 100:
                return n, "", f"manual-pos-{n}"
        except ValueError:
            pass
        print("  Please enter 1-100, 0 (not found), or s (skip).")


SERPER_KEY_FILE = ROOT / "serper_config.json"


def _load_serper_api_key() -> str:
    """Find Serper.dev API key in (a) env var, (b) seo_tracker/serper_config.json.
    Returns empty string if not found."""
    key = os.environ.get("SERPER_API_KEY", "").strip()
    if key:
        return key
    if SERPER_KEY_FILE.exists():
        try:
            data = json.loads(SERPER_KEY_FILE.read_text(encoding="utf-8"))
            return data.get("api_key", "").strip()
        except Exception:
            return ""
    return ""


def provider_serper(query: str, target_domain: str, country: str, lang: str) -> tuple[int, str, str]:
    """Serper.dev — accurate Google data. Reads key from SERPER_API_KEY env var
    or seo_tracker/serper_config.json with {"api_key": "..."}."""
    api_key = _load_serper_api_key()
    if not api_key:
        return RANK_NOT_FOUND, "", "serper-no-api-key (set SERPER_API_KEY env var or create serper_config.json)"
    body = json.dumps({"q": query, "gl": country or "se", "hl": lang or "sv", "num": RANK_TOP_N}).encode("utf-8")
    req = urllib.request.Request(
        "https://google.serper.dev/search",
        data=body,
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        return RANK_NOT_FOUND, "", f"serper-error: {exc.__class__.__name__}"
    target_norm = target_domain.lower().lstrip(".").replace("www.", "")
    for i, item in enumerate(data.get("organic", [])[:RANK_TOP_N], start=1):
        link = item.get("link", "")
        host = urllib.parse.urlparse(link).netloc.lower().replace("www.", "")
        if host == target_norm or host.endswith("." + target_norm):
            return i, link, f"serper-found-pos-{i}"
    return RANK_NOT_FOUND, "", f"serper-checked-{len(data.get('organic', []))}-results"


PROVIDERS = {
    "duckduckgo": provider_duckduckgo,
    "manual": provider_manual,
    "serper": provider_serper,
}


# ---------- Telegram ----------

TELEGRAM_CONFIG_CANDIDATES = [
    Path("c:/Git/ACSIL_Bots/gex/telegram_config.json"),
    ROOT / "telegram_config.json",
    Path.home() / ".telegram_config.json",
]


def _find_telegram_config() -> Path | None:
    for p in TELEGRAM_CONFIG_CANDIDATES:
        if p.exists():
            return p
    return None


def send_telegram(text: str) -> bool:
    """Send a message via Telegram bot. Returns True on success."""
    cfg_path = _find_telegram_config()
    if cfg_path is None:
        print("Telegram skipped: no telegram_config.json found in any candidate path.")
        return False
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        url = f"https://api.telegram.org/bot{cfg['token']}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": cfg["chat_id"],
            "text": text,
        }).encode("utf-8")
        urllib.request.urlopen(url, data=data, timeout=10)
        return True
    except Exception as exc:
        print(f"Telegram send failed: {exc.__class__.__name__}: {exc}")
        return False


# ---------- Commands ----------

def cmd_check(provider_name: str) -> int:
    cfg = load_config()
    domain = cfg["domain"]
    country = cfg.get("country_code", "se")
    lang = cfg.get("language", "sv")
    keywords = cfg["keywords"]
    provider = PROVIDERS.get(provider_name)
    if not provider:
        print(f"Unknown provider: {provider_name}. Choices: {list(PROVIDERS)}")
        return 1

    print("=" * 78)
    print(f"Ranking check — domain: {domain} | provider: {provider_name} | keywords: {len(keywords)}")
    print("=" * 78)

    f, w = history_writer()
    found = 0
    not_found = 0
    try:
        for i, kw in enumerate(keywords, start=1):
            q = kw["q"]
            tier = kw.get("tier", "?")
            sys.stdout.write(f"  [{i:2d}/{len(keywords)}] T{tier} | {q[:48]:48s} ... ")
            sys.stdout.flush()
            rank, found_url, note = provider(q, domain, country, lang)
            if rank > 0:
                print(f"#{rank}")
                found += 1
            else:
                print(f"--  ({note})")
                not_found += 1
            write_history_row(w, kw, provider_name, rank, found_url, note)
            f.flush()
            if provider_name in ("duckduckgo", "serper"):
                time.sleep(2.0)  # rate-limit
    finally:
        f.close()

    print("=" * 78)
    print(f"Done. Found in top {RANK_TOP_N}: {found}  |  Not found: {not_found}")
    print(f"Logged to {HISTORY_PATH.name}")
    print("Run `python ranking_tracker.py report` to regenerate report.html")
    return 0


def cmd_list() -> int:
    cfg = load_config()
    print(f"Domain: {cfg['domain']}  |  Country: {cfg.get('country_code')}  |  Lang: {cfg.get('language')}")
    print(f"Tracked since: {cfg.get('tracked_since', 'unknown')}")
    print(f"Total keywords: {len(cfg['keywords'])}\n")
    for tier in sorted({k.get("tier", 99) for k in cfg["keywords"]}):
        print(f"=== Tier {tier} ===")
        for k in cfg["keywords"]:
            if k.get("tier") == tier:
                print(f"  [{k.get('lang','??')}] {k['q']}  ({k.get('category','-')})")
        print()
    return 0


def cmd_add(query: str) -> int:
    cfg = load_config()
    if any(k["q"].lower() == query.lower() for k in cfg["keywords"]):
        print(f"Already tracked: {query}")
        return 0
    tier = input("  Tier (1=brand 2=local_sv 3=local_en 4=longtail 5=other) [3]: ").strip() or "3"
    category = input("  Category [local_en]: ").strip() or "local_en"
    lang = input("  Lang code (en/sv/fr/de/...) [en]: ").strip() or "en"
    cfg["keywords"].append({"q": query, "tier": int(tier), "category": category, "lang": lang})
    save_config(cfg)
    print(f"Added: {query}")
    return 0


# ---------- Weekly (check + report + telegram summary) ----------

def _summarize_week_over_week(domain: str) -> str:
    """Compare the LAST run with the run before it. Returns a Telegram-ready text."""
    if not HISTORY_PATH.exists():
        return "No history yet."

    rows = list(csv.DictReader(HISTORY_PATH.open("r", encoding="utf-8")))
    if not rows:
        return "History empty."

    # Group by run timestamp (date-precision is sufficient for week-over-week)
    runs: dict[str, list[dict]] = {}
    for r in rows:
        # use date portion of timestamp as the run key
        run_key = r["timestamp_utc"][:10]
        runs.setdefault(run_key, []).append(r)

    run_dates_sorted = sorted(runs.keys())
    latest_date = run_dates_sorted[-1]
    prior_date = run_dates_sorted[-2] if len(run_dates_sorted) >= 2 else None

    latest_by_kw = {r["keyword"]: r for r in runs[latest_date]}
    prior_by_kw = {r["keyword"]: r for r in runs[prior_date]} if prior_date else {}

    new_rankings = []
    improved = []
    worsened = []
    lost = []
    in_top50 = []
    blocked = []

    for kw, latest in latest_by_kw.items():
        latest_rank = int(latest["rank"])
        latest_note = latest.get("note", "")
        if "no-results-parsed" in latest_note or "blocked" in latest_note or "error" in latest_note:
            blocked.append(kw)
            continue
        if latest_rank > 0:
            in_top50.append((kw, latest_rank, latest.get("tier", "?")))

        prior = prior_by_kw.get(kw)
        if prior is None:
            continue
        prior_rank = int(prior["rank"])

        if prior_rank < 0 and latest_rank > 0:
            new_rankings.append((kw, latest_rank, latest.get("tier", "?")))
        elif prior_rank > 0 and latest_rank > 0 and latest_rank < prior_rank:
            improved.append((kw, prior_rank, latest_rank, latest.get("tier", "?")))
        elif prior_rank > 0 and latest_rank > 0 and latest_rank > prior_rank:
            worsened.append((kw, prior_rank, latest_rank, latest.get("tier", "?")))
        elif prior_rank > 0 and latest_rank < 0:
            lost.append((kw, prior_rank, latest.get("tier", "?")))

    # Build the message
    lines = [f"📊 SEO check — {domain}", f"Date: {latest_date} UTC"]
    if prior_date:
        lines.append(f"Compared to: {prior_date}")
    else:
        lines.append("First run — no week-over-week comparison yet.")
    lines.append("")
    lines.append(f"Keywords tracked: {len(latest_by_kw)}")
    lines.append(f"In top 50: {len(in_top50)}")
    if blocked:
        lines.append(f"⚠️ Provider blocked/errored: {len(blocked)} keywords (data unreliable for these)")
    lines.append("")

    if in_top50:
        lines.append("🎯 Currently ranking:")
        for kw, rank, tier in sorted(in_top50, key=lambda x: x[1])[:10]:
            lines.append(f"  #{rank:>3} (T{tier}) {kw}")
        if len(in_top50) > 10:
            lines.append(f"  ...and {len(in_top50) - 10} more (see report.html)")
        lines.append("")

    if new_rankings:
        lines.append("🆕 New this week:")
        for kw, rank, tier in new_rankings[:8]:
            lines.append(f"  #{rank} (T{tier}) {kw}")
        lines.append("")

    if improved:
        lines.append("📈 Improved:")
        for kw, before, after, tier in improved[:8]:
            lines.append(f"  #{before} → #{after} (T{tier}) {kw}")
        lines.append("")

    if worsened:
        lines.append("📉 Slipped:")
        for kw, before, after, tier in worsened[:5]:
            lines.append(f"  #{before} → #{after} (T{tier}) {kw}")
        lines.append("")

    if lost:
        lines.append("❌ Lost from top 50:")
        for kw, before, tier in lost[:5]:
            lines.append(f"  #{before} → ✗ (T{tier}) {kw}")
        lines.append("")

    if not (new_rankings or improved or worsened or lost) and prior_date:
        lines.append("No movement since last check.")

    return "\n".join(lines)


def cmd_weekly(provider_name: str, send_tg: bool = True) -> int:
    """Run check + regenerate report + send Telegram summary. Designed for scheduled use."""
    if provider_name == "manual":
        print("'manual' provider cannot run unattended (needs input). Use duckduckgo or serper.")
        return 1

    print("Weekly run starting...")
    rc = cmd_check(provider_name)
    if rc != 0:
        return rc

    cmd_report()

    cfg = load_config()
    summary = _summarize_week_over_week(cfg["domain"])
    print("\n--- Telegram summary ---")
    print(summary)
    print("--- end summary ---\n")

    if send_tg:
        ok = send_telegram(summary)
        if ok:
            print("Telegram message sent.")
        else:
            print("Telegram NOT sent (see error above).")
    return 0


# ---------- Report ----------

def cmd_report() -> int:
    if not HISTORY_PATH.exists():
        print("No history.csv yet — run `python ranking_tracker.py check` first.")
        return 1

    cfg = load_config()
    rows = list(csv.DictReader(HISTORY_PATH.open("r", encoding="utf-8")))
    # Group by keyword: list of (timestamp, rank, provider) tuples in chrono order
    by_kw: dict[str, list[dict]] = {}
    for r in rows:
        by_kw.setdefault(r["keyword"], []).append(r)
    for kw in by_kw:
        by_kw[kw].sort(key=lambda x: x["timestamp_utc"])

    # Build summary table
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    rows_html = []
    for kw_obj in cfg["keywords"]:
        q = kw_obj["q"]
        history = by_kw.get(q, [])
        if not history:
            latest_rank = "—"
            first_rank = "—"
            arrow = ""
            spark_cells = ""
        else:
            latest = history[-1]
            first = history[0]
            latest_rank = "✗" if int(latest["rank"]) < 0 else f"#{latest['rank']}"
            first_rank = "✗" if int(first["rank"]) < 0 else f"#{first['rank']}"
            # Trend arrow
            lr = int(latest["rank"])
            fr = int(first["rank"])
            if lr > 0 and fr > 0:
                if lr < fr:
                    arrow = '<span style="color:#0a8a3a">▲</span>'
                elif lr > fr:
                    arrow = '<span style="color:#c33">▼</span>'
                else:
                    arrow = '<span style="color:#888">—</span>'
            elif lr > 0 and fr < 0:
                arrow = '<span style="color:#0a8a3a">▲ NEW</span>'
            elif lr < 0 and fr > 0:
                arrow = '<span style="color:#c33">▼ LOST</span>'
            else:
                arrow = ""
            # Sparkline data points
            spark_cells = '<span style="color:#aaa">' + " ".join(
                ("·" if int(h["rank"]) < 0 else str(h["rank"]))
                for h in history[-12:]
            ) + '</span>'

        rows_html.append(
            f'<tr>'
            f'<td>T{kw_obj.get("tier","?")}</td>'
            f'<td>{kw_obj.get("lang","")}</td>'
            f'<td>{q}</td>'
            f'<td>{first_rank}</td>'
            f'<td><strong>{latest_rank}</strong></td>'
            f'<td>{arrow}</td>'
            f'<td class="spark">{spark_cells}</td>'
            f'<td>{len(history)}</td>'
            f'</tr>'
        )

    html = f"""<!doctype html>
<html><head><meta charset="utf-8">
<title>SEO Ranking Tracker — {cfg['domain']}</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 1100px; margin: 2rem auto; padding: 0 1rem; color: #222; }}
  h1 {{ font-size: 1.4rem; margin-bottom: 0.2rem; }}
  .meta {{ color: #777; font-size: 0.9rem; margin-bottom: 1.5rem; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
  th, td {{ text-align: left; padding: 0.5rem 0.6rem; border-bottom: 1px solid #eee; }}
  th {{ background: #f7f4ee; font-weight: 600; }}
  td.spark {{ font-family: ui-monospace, monospace; font-size: 0.8rem; }}
  tr:hover {{ background: #fafafa; }}
  .legend {{ font-size: 0.85rem; color: #666; margin-top: 1.5rem; line-height: 1.6; }}
  code {{ background: #f4f0e8; padding: 0.1em 0.4em; border-radius: 3px; }}
</style>
</head>
<body>
<h1>SEO Ranking Tracker — {cfg['domain']}</h1>
<div class="meta">
  Generated {today} UTC. Tracked since {cfg.get('tracked_since', '?')}.
  History rows: {len(rows)}. Keywords tracked: {len(cfg['keywords'])}.
</div>

<table>
<thead>
<tr><th>Tier</th><th>Lang</th><th>Keyword</th><th>First seen</th><th>Latest</th><th>Trend</th><th>Last 12 checks</th><th>Total</th></tr>
</thead>
<tbody>
{''.join(rows_html)}
</tbody>
</table>

<div class="legend">
  <strong>Legend:</strong>
  <code>#N</code> = position N in search results (lower is better).
  <code>✗</code> = not found in top {RANK_TOP_N}.
  <code>·</code> = check ran but not found.
  <code>▲</code> = improved since first check.
  <code>▼</code> = worse since first check.
  <code>—</code> = unchanged.
  <br><br>
  <strong>Tier meaning:</strong>
  T1 = brand (must rank #1) ·
  T2 = Swedish local intent ·
  T3 = English local intent ·
  T4 = long-tail activity ·
  T5 = other languages
  <br><br>
  <strong>Provider note:</strong> DuckDuckGo data is a free proxy for Google rankings (correlates ~70-85%).
  For accurate Google data, sign up at <code>serper.dev</code> (free 2,500 queries/month), set <code>SERPER_API_KEY</code> env var, and run with <code>--provider serper</code>.
  Or run <code>--provider manual</code> and type positions you see in incognito Google.
</div>
</body></html>
"""
    REPORT_PATH.write_text(html, encoding="utf-8")
    print(f"Report regenerated: {REPORT_PATH}")
    print(f"Open in browser: file:///{REPORT_PATH.as_posix()}")
    return 0


# ---------- Main ----------

def main() -> int:
    p = argparse.ArgumentParser(description="SEO ranking tracker")
    p.add_argument("command", choices=["check", "weekly", "report", "list", "add"], help="What to do")
    p.add_argument("query", nargs="?", default="", help="Keyword for `add`")
    p.add_argument("--provider", default="duckduckgo",
                   choices=list(PROVIDERS), help="Search provider for `check` / `weekly`")
    p.add_argument("--no-telegram", action="store_true",
                   help="Skip Telegram for `weekly` (still runs check + report)")
    args = p.parse_args()

    if args.command == "check":
        return cmd_check(args.provider)
    if args.command == "weekly":
        return cmd_weekly(args.provider, send_tg=not args.no_telegram)
    if args.command == "report":
        return cmd_report()
    if args.command == "list":
        return cmd_list()
    if args.command == "add":
        if not args.query:
            print("Usage: python ranking_tracker.py add \"keyword text\"")
            return 1
        return cmd_add(args.query)
    return 0


if __name__ == "__main__":
    sys.exit(main())
