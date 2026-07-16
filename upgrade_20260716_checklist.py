# -*- coding: utf-8 -*-
"""Checklist-driven SEO round 2, 2026-07-16 — from the global website checklist
(C:/Users/skibi/.claude/knowledge/website/CHECKLIST.md). Companion new files
committed alongside: llms.txt, terms.html, favicon.svg.

Per language file:
  - <title> trimmed to <=60 chars where over (EN was 64, DE 61)
  - <meta name="referrer"> (Referrer-Policy — GitHub Pages can't send headers)
  - SVG favicon link (SVG + PNG/ICO fallback per checklist)
  - money keywords into two H2s (accommodation, experiences)
  - footer: link to /terms.html + visible freshness stamp
Sitemap: terms.html added, lastmod bumped.

Usage: python upgrade_20260716_checklist.py   (repo root, run ONCE — not idempotent)
"""
import re
import sys
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent
LASTMOD = "2026-07-16T15:00:00Z"
STAMP = "2026-07-16"
ERRORS = []

L = {
    "en": dict(
        file="index.html",
        title="Stations Hotellet — Apartment Öjebyn/Piteå, Swedish Lapland",
        h2_acc="Your Apartment in Öjebyn — 2 Bedrooms, Sleeps 5",
        h2_exp="Things to do in Piteå &amp; Swedish Lapland",
        terms="Booking terms",
        updated=f"Prices &amp; info updated {STAMP}",
    ),
    "sv": dict(
        file="sv/index.html",
        title=None,  # 58 chars, fine
        h2_acc="Din lägenhet i Öjebyn — 2 sovrum, plats för 5",
        h2_exp="Saker att göra i Piteå och Norrbotten",
        terms="Bokningsvillkor",
        updated=f"Priser &amp; info uppdaterade {STAMP}",
    ),
    "fr": dict(
        file="fr/index.html",
        title=None,  # 59 chars, fine
        h2_acc="Votre appartement à Öjebyn — 2 chambres, 5 personnes",
        h2_exp="Que faire à Piteå et en Laponie suédoise",
        terms="Conditions de réservation",
        updated=f"Infos et prix mis à jour le {STAMP}",
    ),
    "de": dict(
        file="de/index.html",
        title="Stations Hotellet — Ferienwohnung Piteå, Schwedisch-Lappland",
        h2_acc="Ihre Ferienwohnung in Öjebyn — 2 Schlafzimmer, bis zu 5 Gäste",
        h2_exp="Aktivitäten in Piteå &amp; Schwedisch-Lappland",
        terms="Buchungsbedingungen",
        updated=f"Preise &amp; Infos aktualisiert am {STAMP}",
    ),
    "pl": dict(
        file="pl/index.html",
        title=None,  # 56 chars, fine
        h2_acc="Twój apartament w Öjebyn — 2 sypialnie, do 5 osób",
        h2_exp="Atrakcje w Piteå i szwedzkiej Laponii",
        terms="Warunki rezerwacji",
        updated=f"Ceny i informacje zaktualizowane {STAMP}",
    ),
    "ro": dict(
        file="ro/index.html",
        title=None,  # 55 chars, fine
        h2_acc="Apartamentul tău din Öjebyn — 2 dormitoare, până la 5 persoane",
        h2_exp="Ce poți face în Piteå și Laponia suedeză",
        terms="Condiții de rezervare",
        updated=f"Prețuri și informații actualizate la {STAMP}",
    ),
}


def rep(text, pattern, repl_fn, want, desc, fname):
    new, n = re.subn(pattern, repl_fn, text)
    if n != want:
        ERRORS.append(f"{fname}: {desc} matched {n}x (expected {want})")
        return text
    return new


for lang, d in L.items():
    path = REPO / d["file"]
    t = path.read_text(encoding="utf-8")
    fname = d["file"]

    if d["title"]:
        if len(d["title"]) > 60:
            ERRORS.append(f"{fname}: replacement title is {len(d['title'])} chars (>60)")
        t = rep(t, r"<title>[\s\S]*?</title>",
                lambda m: f"<title>{d['title']}</title>", 1, "title", fname)

    t = rep(t, r'(<meta name="theme-color" content="[^"]*">)',
            lambda m: m.group(1) + '\n    <meta name="referrer" content="strict-origin-when-cross-origin">',
            1, "referrer meta", fname)

    t = rep(t, r'(<link rel="icon" href="/favicon\.ico" sizes="48x48">)',
            lambda m: '<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n    ' + m.group(1),
            1, "svg favicon link", fname)

    t = rep(t, r'(id="accommodation">[\s\S]*?<h2 class="section-title">)[\s\S]*?(</h2>)',
            lambda m: m.group(1) + d["h2_acc"] + m.group(2), 1, "H2 accommodation", fname)

    t = rep(t, r'(id="experiences">[\s\S]*?<h2 class="section-title">)[\s\S]*?(</h2>)',
            lambda m: m.group(1) + d["h2_exp"] + m.group(2), 1, "H2 experiences", fname)

    footer_p = (f'    <p style="margin-top: 0.5rem;"><a href="/terms.html">{d["terms"]}</a>'
                f' &middot; {d["updated"]}</p>\n')
    t = rep(t, r"</footer>", lambda m: footer_p + "</footer>", 1, "footer terms+stamp", fname)

    path.write_text(t, encoding="utf-8", newline="\n")
    print(f"  OK {fname}")

# --- sitemap: bump lastmod + add terms.html
sm = REPO / "sitemap.xml"
t = sm.read_text(encoding="utf-8")
t, n = re.subn(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{LASTMOD}</lastmod>", t)
print(f"  sitemap: {n} lastmod bumped")
terms_entry = f"""  <url>
    <loc>https://stationshotellet.com/terms.html</loc>
    <lastmod>{LASTMOD}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>"""
t, n = re.subn(r"</urlset>", terms_entry, t)
if n != 1:
    ERRORS.append(f"sitemap.xml: urlset close matched {n}x")
sm.write_text(t, encoding="utf-8", newline="\n")
print("  OK sitemap.xml (+terms.html)")

# --- validation
print("--- validation ---")
for lang, d in L.items():
    t = (REPO / d["file"]).read_text(encoding="utf-8")
    title = re.search(r"<title>([\s\S]*?)</title>", t).group(1)
    if len(title) > 60:
        ERRORS.append(f"{d['file']}: title still {len(title)} chars: {title}")
    for needle, want in [
        ('name="referrer"', 1), ("favicon.svg", 1), ('href="/terms.html"', 1),
        (d["h2_acc"], 1), (d["h2_exp"], 1),
    ]:
        got = t.count(needle)
        if got != want:
            ERRORS.append(f"{d['file']}: '{needle[:40]}' count {got} (want {want})")
    for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', t):
        try:
            json.loads(m.group(1))
        except json.JSONDecodeError as e:
            ERRORS.append(f"{d['file']}: JSON-LD broken: {e}")
    print(f"  checked {d['file']} (title {len(title)} chars)")

smt = sm.read_text(encoding="utf-8")
if smt.count("<url>") != 7:
    ERRORS.append(f"sitemap: {smt.count('<url>')} url blocks (want 7)")

if ERRORS:
    print("\n!!! ERRORS:")
    for e in ERRORS:
        print("  -", e)
    sys.exit(1)
print("\nALL GOOD")
