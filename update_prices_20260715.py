# -*- coding: utf-8 -*-
"""Price update 2026-07-15 (Soren's decision): weekly 5,500 -> 6,500 kr,
monthly 14,000 -> 19,000 kr. Nightly unchanged at 990 kr.

Derived numbers (all recomputed):
  weekly  6,500 kr = 929 kr/night = save 6%  vs 7x990 (6,930)
  monthly 19,000 kr = 633 kr/night = save 36% vs 30x990 (29,700)

Touches per language file: price cards, data-sek EUR attributes, JSON-LD offers
+ priceRange, EN FAQ schema price answer. Also bumps sitemap lastmod.

Context-anchored replacements only — bare numbers are traps here:
&#127869; (emoji entity) contains "786"; phone +46706718185 contains "467".

Usage: python update_prices_20260715.py   (repo root, run ONCE — not idempotent)
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
FILES = ["index.html", "sv/index.html", "fr/index.html",
         "de/index.html", "pl/index.html", "ro/index.html"]
LASTMOD = "2026-07-15T03:10:00Z"
ERRORS = []


def rep(text, pattern, repl, want, desc, fname, flags=0):
    new, n = re.subn(pattern, repl, text, flags=flags)
    if n != want:
        ERRORS.append(f"{fname}: {desc} matched {n}x (expected {want})")
        return text
    return new


for fname in FILES:
    path = REPO / fname
    t = path.read_text(encoding="utf-8")
    en = fname == "index.html"

    # --- visible card amounts (separator preserved via group)
    t = rep(t, r"5(\s|&nbsp;)?500 kr", lambda m: f"6{m.group(1) or ''}500 kr", 1,
            "weekly amount", fname)
    t = rep(t, r"14(\s|&nbsp;)?000 kr", lambda m: f"19{m.group(1) or ''}000 kr", 1,
            "monthly amount", fname)

    # --- per-night derivations (card unit lines + EN FAQ answer share the pattern)
    t = rep(t, r"786 kr/", "929 kr/", 2 if en else 1, "786 kr/night", fname)
    t = rep(t, r"467 kr/", "633 kr/", 2 if en else 1, "467 kr/night", fname)

    # --- EN FAQ schema comma-formatted amounts
    # 14,000 kr appears twice: price answer + healthcare-staff answer
    if en:
        t = rep(t, r"5,500 kr", "6,500 kr", 1, "FAQ weekly amount", fname)
        t = rep(t, r"14,000 kr", "19,000 kr", 2, "FAQ monthly amount", fname)

    # --- EUR converter attributes
    t = rep(t, r'data-sek="5500"', 'data-sek="6500"', 1, "data-sek weekly", fname)
    t = rep(t, r'data-sek="14000"', 'data-sek="19000"', 1, "data-sek monthly", fname)

    # --- JSON-LD: priceRange first (exact), then quoted offer prices
    t = rep(t, r"990–14000 SEK", "990–19000 SEK", 1, "priceRange", fname)
    t = rep(t, r'"5500"', '"6500"', 2, "JSON weekly price", fname)
    t = rep(t, r'"14000"', '"19000"', 2, "JSON monthly price", fname)
    t = rep(t, r"save 21% vs nightly", "save 6% vs nightly", 1,
            "JSON weekly offer description", fname)

    # --- visible save-% lines, bounded to the prices section only
    i0 = t.find('id="prices"')
    i1 = t.find('id="booking"')
    if i0 == -1 or i1 == -1 or i1 <= i0:
        ERRORS.append(f"{fname}: prices section bounds not found")
    else:
        seg = t[i0:i1]
        seg = rep(seg, r"21(\s?%)", lambda m: "6" + m.group(1), 1,
                  "card weekly save-%", fname)
        seg = rep(seg, r"53(\s?%)", lambda m: "36" + m.group(1), 1,
                  "card monthly save-%", fname)
        t = t[:i0] + seg + t[i1:]

    path.write_text(t, encoding="utf-8", newline="\n")
    print(f"  OK {fname}")

# --- sitemap
sm = REPO / "sitemap.xml"
t = sm.read_text(encoding="utf-8")
t, n = re.subn(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{LASTMOD}</lastmod>", t)
sm.write_text(t, encoding="utf-8", newline="\n")
print(f"  OK sitemap.xml ({n} lastmod -> {LASTMOD})")

# --- validation: old numbers must be gone from price contexts, new ones present
import json
print("--- validation ---")
for fname in FILES:
    t = (REPO / fname).read_text(encoding="utf-8")
    for bad in [r"5(\s|&nbsp;)?500 kr", r"786 kr/", r'data-sek="5500"',
                r'"5500"', r"990–14000", r"save 21%", r"467 kr/", r'"14000"']:
        if re.search(bad, t):
            ERRORS.append(f"{fname}: stale pattern still present: {bad}")
    for good, want in [(r"6(\s|&nbsp;)?500 kr", 1), (r"929 kr/", 2 if fname == "index.html" else 1),
                       (r"19(\s|&nbsp;)?000 kr", 1), (r"633 kr/", 2 if fname == "index.html" else 1),
                       (r'data-sek="6500"', 1), (r'data-sek="19000"', 1),
                       (r"990–19000 SEK", 1)]:
        n = len(re.findall(good, t))
        if n != want:
            ERRORS.append(f"{fname}: new pattern {good} count {n} (expected {want})")
    for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', t):
        try:
            json.loads(m.group(1))
        except json.JSONDecodeError as e:
            ERRORS.append(f"{fname}: JSON-LD broken after edit: {e}")
    print(f"  checked {fname}")

if ERRORS:
    print("\n!!! ERRORS:")
    for e in ERRORS:
        print("  -", e)
    sys.exit(1)
print("\nALL GOOD")
