# -*- coding: utf-8 -*-
"""Price update round 2, 2026-07-15 (Soren): weekly 6,500 -> 6,200 kr,
monthly 19,000 -> 23,800 kr. Nightly unchanged at 990 kr.

Ladder rationale: ~10% / ~20% savings vs nightly (Soren's chosen structure):
  weekly  6,200 kr = 886 kr/night = 10.5% off 7x990 (6,930)  -> card says 10%
  monthly 23,800 kr = 793 kr/night = 19.9% off 30x990 (29,700) -> card says 20%

Replaces the 6,500/19,000 values deployed a few hours earlier (see
update_prices_20260715.py). Context-anchored patterns only.
NOTE: replace 36% BEFORE 6% and use a digit-boundary — "36%" contains "6%".

Usage: python update_prices_20260715b.py   (repo root, run ONCE — not idempotent)
"""
import re
import sys
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent
FILES = ["index.html", "sv/index.html", "fr/index.html",
         "de/index.html", "pl/index.html", "ro/index.html"]
LASTMOD = "2026-07-15T04:15:00Z"
ERRORS = []


def rep(text, pattern, repl, want, desc, fname):
    new, n = re.subn(pattern, repl, text)
    if n != want:
        ERRORS.append(f"{fname}: {desc} matched {n}x (expected {want})")
        return text
    return new


for fname in FILES:
    path = REPO / fname
    t = path.read_text(encoding="utf-8")
    en = fname == "index.html"

    t = rep(t, r"6(\s|&nbsp;)?500 kr", lambda m: f"6{m.group(1) or ''}200 kr", 1,
            "weekly amount", fname)
    t = rep(t, r"19(\s|&nbsp;)?000 kr", lambda m: f"23{m.group(1) or ''}800 kr", 1,
            "monthly amount", fname)
    t = rep(t, r"929 kr/", "886 kr/", 2 if en else 1, "weekly per-night", fname)
    t = rep(t, r"633 kr/", "793 kr/", 2 if en else 1, "monthly per-night", fname)
    if en:
        t = rep(t, r"6,500 kr", "6,200 kr", 1, "FAQ weekly amount", fname)
        t = rep(t, r"19,000 kr", "23,800 kr", 2, "FAQ monthly amounts", fname)
    t = rep(t, r'data-sek="6500"', 'data-sek="6200"', 1, "data-sek weekly", fname)
    t = rep(t, r'data-sek="19000"', 'data-sek="23800"', 1, "data-sek monthly", fname)
    t = rep(t, r"990–19000 SEK", "990–23800 SEK", 1, "priceRange", fname)
    t = rep(t, r'"6500"', '"6200"', 2, "JSON weekly price", fname)
    t = rep(t, r'"19000"', '"23800"', 2, "JSON monthly price", fname)
    t = rep(t, r"save 6% vs nightly", "save 10% vs nightly", 1,
            "JSON weekly offer description", fname)

    i0 = t.find('id="prices"')
    i1 = t.find('id="booking"')
    if i0 == -1 or i1 == -1 or i1 <= i0:
        ERRORS.append(f"{fname}: prices section bounds not found")
    else:
        seg = t[i0:i1]
        # 36% FIRST (contains a "6%" substring), then digit-bounded 6%
        seg = rep(seg, r"36(\s?%)", lambda m: "20" + m.group(1), 1,
                  "card monthly save-%", fname)
        seg = rep(seg, r"(?<![0-9])6(\s?%)", lambda m: "10" + m.group(1), 1,
                  "card weekly save-%", fname)
        t = t[:i0] + seg + t[i1:]

    path.write_text(t, encoding="utf-8", newline="\n")
    print(f"  OK {fname}")

sm = REPO / "sitemap.xml"
t = sm.read_text(encoding="utf-8")
t, n = re.subn(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{LASTMOD}</lastmod>", t)
sm.write_text(t, encoding="utf-8", newline="\n")
print(f"  OK sitemap.xml ({n} lastmod -> {LASTMOD})")

print("--- validation ---")
for fname in FILES:
    t = (REPO / fname).read_text(encoding="utf-8")
    en = fname == "index.html"
    for bad in [r"6(\s|&nbsp;)?500 kr", r"6,500 kr", r"929 kr/", r'data-sek="6500"',
                r'"6500"', r"990–19000", r"save 6%", r"633 kr/", r'"19000"',
                r"19(\s|&nbsp;)?000 kr", r"19,000 kr", r'data-sek="19000"']:
        if re.search(bad, t):
            ERRORS.append(f"{fname}: stale: {bad}")
    for good, want in [
        (r"6(\s|&nbsp;)?200 kr", 1), (r"886 kr/", 2 if en else 1),
        (r"23(\s|&nbsp;)?800 kr", 1), (r"793 kr/", 2 if en else 1),
        (r'data-sek="6200"', 1), (r'data-sek="23800"', 1),
        (r"990–23800 SEK", 1), (r'"6200"', 3), (r'"23800"', 3),
        (r"save 10% vs nightly", 1),
    ]:
        cnt = len(re.findall(good, t))
        if cnt != want:
            ERRORS.append(f"{fname}: {good} count {cnt} (want {want})")
    for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', t):
        try:
            json.loads(m.group(1))
        except json.JSONDecodeError as e:
            ERRORS.append(f"{fname}: JSON-LD broken: {e}")
    print(f"  checked {fname}")

if ERRORS:
    print("\n!!! ERRORS:")
    for e in ERRORS:
        print("  -", e)
    sys.exit(1)
print("\nALL GOOD — weekly 6,200 (10%) / monthly 23,800 (20%), nightly 990")
