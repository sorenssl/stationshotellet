# -*- coding: utf-8 -*-
"""Overnight-keyword weave, 2026-07-31 — Soren's pick: "övernattning Piteå".

Audit before this run: sv page had 'övernattning' 4x (none in title/description/
headings), EN page had 'overnight' ZERO times. This weaves each language's
everyday overnight-stay word into prime spots:
  - sv <title> + meta description now lead with övernattning
  - new FAQ item (visible + FAQPage schema) in ALL 6 languages, built around
    övernattning / overnight stay / Übernachtung / nuitée / nocleg / cazare
  - tracker config: +övernattning Piteå (T2), +Übernachtung Piteå, +nocleg Piteå (T5)

Usage: python update_overnight_20260731.py   (repo root, ONCE — not idempotent)
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
LASTMOD = "2026-07-31T15:10:00Z"
ERRORS = []

FAQ = {
    "en": ("index.html",
           "Is Stations Hotellet good for a one-night overnight stay?",
           "Absolutely — a single overnight stay is as welcome as a long one. 990 kr for the whole apartment (up to 5 guests), lockbox check-in at any hour and free parking, just off the E4 — a perfect stopover on the drive through northern Sweden."),
    "sv": ("sv/index.html",
           "Passar Stations Hotellet för en natts övernattning i Piteå?",
           "Absolut — en natts övernattning är lika välkommen som en lång vistelse. 990 kr för hela lägenheten (upp till 5 gäster), incheckning med nyckelbox när det passar dig och gratis parkering nära E4 — perfekta stoppet på resan genom Norrbotten."),
    "fr": ("fr/index.html",
           "Peut-on réserver une seule nuitée au Stations Hotellet ?",
           "Bien sûr — une seule nuitée est aussi bienvenue qu'un long séjour. 990 kr pour l'appartement entier (jusqu'à 5 personnes), arrivée autonome à toute heure et parking gratuit près de la E4 — l'étape idéale sur la route du nord de la Suède."),
    "de": ("de/index.html",
           "Eignet sich das Stations Hotellet für eine Übernachtung auf der Durchreise?",
           "Absolut — eine einzelne Übernachtung ist genauso willkommen wie ein langer Aufenthalt. 990 kr für die ganze Wohnung (bis zu 5 Gäste), Schlüsselbox-Check-in rund um die Uhr und Gratisparkplatz nahe der E4 — der perfekte Zwischenstopp in Nordschweden."),
    "pl": ("pl/index.html",
           "Czy Stations Hotellet nadaje się na nocleg na jedną noc w Piteå?",
           "Jak najbardziej — nocleg na jedną noc jest równie mile widziany jak dłuższy pobyt. 990 kr za cały apartament (do 5 osób), zameldowanie skrytką o dowolnej porze i darmowy parking przy trasie E4 — idealny przystanek w podróży przez północną Szwecję."),
    "ro": ("ro/index.html",
           "Se poate rezerva o singură noapte de cazare la Stations Hotellet?",
           "Desigur — cazarea pentru o singură noapte este la fel de binevenită ca un sejur lung. 990 kr pentru întregul apartament (până la 5 oaspeți), check-in cu cutie de chei la orice oră și parcare gratuită lângă E4 — oprirea perfectă în drumul prin nordul Suediei."),
}

SV_TITLE = "Stations Hotellet — Lägenhet & övernattning i Öjebyn, Piteå"
SV_DESC = "Övernattning i Piteå — lägenhet med 2 sovrum i en ombyggd järnvägsstation i Öjebyn. Norrsken på vintern, Pite Havsbad på sommaren. Från 990 kr/natt — allt ingår."

for lang, (fname, q, a) in FAQ.items():
    path = REPO / fname
    t = path.read_text(encoding="utf-8")

    # sv: title + description lead with övernattning
    if lang == "sv":
        if len(SV_TITLE) > 60:
            ERRORS.append(f"sv title {len(SV_TITLE)} chars")
        t, n = re.subn(r"<title>[\s\S]*?</title>", f"<title>{SV_TITLE}</title>", t, count=1)
        if n != 1:
            ERRORS.append("sv: title replace failed")
        t, n = re.subn(r'<meta name="description" content="[^"]*">',
                       f'<meta name="description" content="{SV_DESC}">', t, count=1)
        if n != 1:
            ERRORS.append("sv: description replace failed")

    # visible FAQ: insert new item after the LAST </details> in the faq section
    i0 = t.find('<section id="faq">')
    i1 = t.find("</section>", i0)
    if i0 == -1 or i1 == -1:
        ERRORS.append(f"{fname}: faq section not found")
    else:
        seg = t[i0:i1]
        last = seg.rfind("</details>")
        if last == -1:
            ERRORS.append(f"{fname}: no </details> in faq section")
        else:
            item = (f"\n            <details class=\"faq-item\">\n"
                    f"                <summary>{q}</summary>\n"
                    f"                <p>{a}</p>\n"
                    f"            </details>")
            insert_at = i0 + last + len("</details>")
            t = t[:insert_at] + item + t[insert_at:]

    # FAQPage schema: append the same Q&A
    blocks = list(re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', t))
    faq_block = None
    for m in blocks:
        if '"FAQPage"' in m.group(1):
            faq_block = m
            break
    if not faq_block:
        ERRORS.append(f"{fname}: FAQPage schema not found")
    else:
        data = json.loads(faq_block.group(1))
        data["mainEntity"].append({
            "@type": "Question", "name": q.replace("&amp;", "&"),
            "acceptedAnswer": {"@type": "Answer", "text": a.replace("&amp;", "&")},
        })
        new_block = ('<script type="application/ld+json">\n'
                     + json.dumps(data, ensure_ascii=False, indent=4)
                     + "\n    </script>")
        t = t[:faq_block.start()] + new_block + t[faq_block.end():]

    path.write_text(t, encoding="utf-8", newline="\n")
    print(f"  OK {fname}")

# sitemap bump
sm = REPO / "sitemap.xml"
t = sm.read_text(encoding="utf-8")
t, n = re.subn(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{LASTMOD}</lastmod>", t)
sm.write_text(t, encoding="utf-8", newline="\n")
print(f"  OK sitemap.xml ({n} lastmod)")

# tracker config: three new keywords
cfg = REPO / "seo_tracker" / "config.json"
t = cfg.read_text(encoding="utf-8")
anchor = '{"q": "billig övernattning Piteå", "tier": 2, "category": "local_sv", "lang": "sv"},'
if anchor not in t:
    ERRORS.append("config: sv anchor not found")
else:
    t = t.replace(anchor, anchor + '\n    {"q": "övernattning Piteå", "tier": 2, "category": "local_sv", "lang": "sv"},', 1)
anchor2 = '{"q": "Ferienwohnung Piteå", "tier": 5, "category": "local_other", "lang": "de"}'
if anchor2 not in t:
    ERRORS.append("config: de anchor not found")
else:
    t = t.replace(anchor2, anchor2 + ',\n    {"q": "Übernachtung Piteå", "tier": 5, "category": "local_other", "lang": "de"},\n    {"q": "nocleg Piteå", "tier": 5, "category": "local_other", "lang": "pl"}', 1)
json.loads(t)  # must still be valid JSON
cfg.write_text(t, encoding="utf-8", newline="\n")
print("  OK config.json (+3 keywords, JSON valid)")

# validation
print("--- validation ---")
for lang, (fname, q, a) in FAQ.items():
    t = (REPO / fname).read_text(encoding="utf-8")
    if t.count(q) != 2:  # visible + schema
        ERRORS.append(f"{fname}: question count {t.count(q)} (want 2)")
    if t.count('<details class="faq-item">') != 7:
        ERRORS.append(f"{fname}: faq items {t.count(chr(60) + 'details class=')} (want 7)")
    for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', t):
        json.loads(m.group(1))
    print(f"  checked {fname}")
sv = (REPO / "sv/index.html").read_text(encoding="utf-8")
print(f"  sv övernattning count now: {len(re.findall('övernattning', sv, re.IGNORECASE))}")

if ERRORS:
    print("\n!!! ERRORS:")
    for e in ERRORS:
        print("  -", e)
    sys.exit(1)
print("\nALL GOOD")
