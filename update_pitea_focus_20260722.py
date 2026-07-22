# -*- coding: utf-8 -*-
"""Piteå-first rebalance, 2026-07-22 (Soren's call after seeing SERP competitors).

Rationale: tracker 2026-07-19 shows we rank where competition is thin
("accommodation Öjebyn" #3) but nowhere on Piteå terms — that wall is mostly
authority (Booking/Airbnb/hotels), yet the H1 (strongest on-page element) still
led with Öjebyn only. This shifts the most prominent copy toward Piteå while
keeping claims honest: "lowest WHOLE-APARTMENT rates in the PITEÅ AREA"
(hostel beds exist from ~590 kr, so a bare "cheapest in Piteå" would be false;
May-2026 comp research: cheapest whole 2BR within 30 km = us).

Touches per language: H1 (Öjebyn -> Piteå (Öjebyn)), hero paragraph,
prices H2, og:title, JSON-LD description claim. Sitemap lastmod bump.

Usage: python update_pitea_focus_20260722.py   (repo root, ONCE — not idempotent)
"""
import re
import sys
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent
LASTMOD = "2026-07-22T13:15:00Z"
ERRORS = []

L = {
    "en": dict(
        file="index.html",
        og_title="Stations Hotellet — Railway Station Apartment in Piteå, Swedish Lapland",
        hero_p="The Piteå area's lowest whole-apartment rates — 2 bedrooms, sleeps 5. From <strong>990&nbsp;kr/night all-inclusive</strong> — cleaning, Wi-Fi and parking included. Your base for northern lights, Pite Havsbad beaches and Swedish Lapland adventures.",
        prices_h2="Lowest Whole-Apartment Rates in the Piteå Area — All-Inclusive",
        ld_old="Lowest direct-book rates in Öjebyn",
        ld_new="The Piteå area's lowest whole-apartment direct-book rates",
    ),
    "sv": dict(
        file="sv/index.html",
        og_title="Stations Hotellet — Lägenhet i järnvägsstation, Piteå (Öjebyn)",
        hero_p="Piteå-områdets lägsta pris för hel lägenhet — 2 sovrum, upp till 5 gäster. Från <strong>990&nbsp;kr/natt — allt ingår</strong>: städning, Wi-Fi och parkering. Perfekt bas för norrsken, Pite Havsbad och äventyr i Norrbotten.",
        prices_h2="Lägsta priset för hel lägenhet i Piteå-området — allt ingår",
        ld_old="Lägsta direktbokningspriserna i Öjebyn",
        ld_new="Piteå-områdets lägsta direktbokningspris för hel lägenhet",
    ),
    "fr": dict(
        file="fr/index.html",
        og_title="Stations Hotellet — Appartement dans une ancienne gare à Piteå, Laponie suédoise",
        hero_p="Le meilleur prix de la région de Piteå pour un appartement entier — 2 chambres, jusqu'à 5 personnes. Dès <strong>990&nbsp;kr/nuit tout inclus</strong> — ménage, Wi-Fi et parking compris. Votre camp de base pour les aurores boréales, Pite Havsbad et la Laponie suédoise.",
        prices_h2="Le meilleur prix pour un appartement entier dans la région de Piteå — tout inclus",
        ld_old="Les meilleurs tarifs en réservation directe à Öjebyn",
        ld_new="Le meilleur tarif de la région de Piteå en réservation directe pour un appartement entier",
    ),
    "de": dict(
        file="de/index.html",
        og_title="Stations Hotellet — Ferienwohnung im alten Bahnhof, Piteå, Schwedisch-Lappland",
        hero_p="Der günstigste Preis der Region Piteå für eine ganze Wohnung — 2 Schlafzimmer, bis zu 5 Gäste. Ab <strong>990&nbsp;kr/Nacht, alles inklusive</strong> — Reinigung, WLAN und Parkplatz inbegriffen. Ihre Basis für Polarlichter, Pite Havsbad und Schwedisch-Lappland.",
        prices_h2="Günstigste ganze Wohnung der Region Piteå — alles inklusive",
        ld_old="Die günstigsten Direktbuchungspreise in Öjebyn",
        ld_new="Der günstigste Direktbuchungspreis der Region Piteå für eine ganze Wohnung",
    ),
    "pl": dict(
        file="pl/index.html",
        og_title="Stations Hotellet — Apartament na dawnym dworcu, Piteå, szwedzka Laponia",
        hero_p="Najniższa cena w rejonie Piteå za cały apartament — 2 sypialnie, do 5 gości. Od <strong>990&nbsp;kr/noc, wszystko w cenie</strong> — sprzątanie, Wi-Fi i parking. Idealna baza na zorzę polarną, Pite Havsbad i przygody w szwedzkiej Laponii.",
        prices_h2="Najtańszy cały apartament w rejonie Piteå — wszystko w cenie",
        ld_old="Najniższe ceny rezerwacji bezpośredniej w Öjebyn",
        ld_new="Najniższa cena rezerwacji bezpośredniej całego apartamentu w rejonie Piteå",
    ),
    "ro": dict(
        file="ro/index.html",
        og_title="Stations Hotellet — Apartament în gara veche, Piteå, Laponia suedeză",
        hero_p="Cel mai bun preț din zona Piteå pentru un apartament întreg — 2 dormitoare, până la 5 oaspeți. De la <strong>990&nbsp;kr/noapte, totul inclus</strong> — curățenie, Wi-Fi și parcare. Baza ta pentru aurora boreală, Pite Havsbad și aventuri în Laponia suedeză.",
        prices_h2="Cel mai bun preț pentru un apartament întreg din zona Piteå — totul inclus",
        ld_old="Cele mai bune prețuri la rezervare directă în Öjebyn",
        ld_new="Cel mai bun preț la rezervare directă pentru un apartament întreg din zona Piteå",
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

    # H1: Öjebyn -> Piteå (Öjebyn), only inside the h1
    m = re.search(r"<h1>[\s\S]*?</h1>", t)
    if not m:
        ERRORS.append(f"{fname}: no h1")
    else:
        h1 = m.group(0)
        if "Piteå" in h1:
            ERRORS.append(f"{fname}: h1 already contains Piteå: {h1[:80]}")
        elif h1.count("Öjebyn") != 1:
            ERRORS.append(f"{fname}: h1 Öjebyn count {h1.count('Öjebyn')}: {h1[:80]}")
        else:
            t = t.replace(h1, h1.replace("Öjebyn", "Piteå (Öjebyn)"), 1)

    t = rep(t, r'<meta property="og:title" content="[^"]*">',
            lambda mm: f'<meta property="og:title" content="{d["og_title"]}">',
            1, "og:title", fname)

    t = rep(t, r'(<section class="hero"[\s\S]*?<h1>[\s\S]*?</h1>\s*<p>)[\s\S]*?(</p>)',
            lambda mm: mm.group(1) + d["hero_p"] + mm.group(2), 1, "hero paragraph", fname)

    t = rep(t, r'(id="prices">[\s\S]*?<h2 class="section-title">)[\s\S]*?(</h2>)',
            lambda mm: mm.group(1) + d["prices_h2"] + mm.group(2), 1, "prices H2", fname)

    if t.count(d["ld_old"]) != 1:
        ERRORS.append(f"{fname}: JSON-LD claim '{d['ld_old'][:40]}' count {t.count(d['ld_old'])}")
    else:
        t = t.replace(d["ld_old"], d["ld_new"], 1)

    path.write_text(t, encoding="utf-8", newline="\n")
    print(f"  OK {fname}")

sm = REPO / "sitemap.xml"
t = sm.read_text(encoding="utf-8")
t, n = re.subn(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{LASTMOD}</lastmod>", t)
sm.write_text(t, encoding="utf-8", newline="\n")
print(f"  OK sitemap.xml ({n} lastmod)")

print("--- validation ---")
for lang, d in L.items():
    t = (REPO / d["file"]).read_text(encoding="utf-8")
    h1 = re.search(r"<h1>[\s\S]*?</h1>", t).group(0)
    if "Piteå (Öjebyn)" not in h1:
        ERRORS.append(f"{d['file']}: h1 not rebalanced: {h1[:90]}")
    for needle, want in [(d["prices_h2"], 1), (d["ld_new"], 1), (d["og_title"], 1)]:
        if t.count(needle) != want:
            ERRORS.append(f"{d['file']}: '{needle[:40]}' count {t.count(needle)}")
    for mm in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', t):
        try:
            json.loads(mm.group(1))
        except json.JSONDecodeError as e:
            ERRORS.append(f"{d['file']}: JSON-LD broken: {e}")
    print(f"  checked {d['file']}: h1 = {re.sub(r'<[^>]+>|&nbsp;', ' ', h1).strip()}")

if ERRORS:
    print("\n!!! ERRORS:")
    for e in ERRORS:
        print("  -", e)
    sys.exit(1)
print("\nALL GOOD")
