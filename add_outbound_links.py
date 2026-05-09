"""Add outbound links to selected cards across all 6 language versions.

Maps each card (identified by its language-specific <h3> text) to a verified
authority URL. Inserts a styled .outbound link before the card's closing </div>.

Idempotent: if the link is already present (anywhere in the card body),
the card is skipped.

URLs were liveness-tested with curl HEAD before this script was written.
Only 200-status URLs are included.

Run from repo root: python add_outbound_links.py
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent

# Each entry: card_h3_text_per_language → (url, display_text)
# h3 text identifies the card uniquely within a file.
# The script inserts an <a class="outbound" ...> just before the card's </div>.

LINKS = {
    # --- Things to do ---
    "aurora": {
        "url": "https://www.swedishlapland.com/things-to-do/",
        "display": "swedishlapland.com →",
        "h3": {
            "index.html":    "Aurora Borealis",
            "sv/index.html": "Norrsken",
            "fr/index.html": "Aurores boréales",
            "de/index.html": "Nordlichter",
            "pl/index.html": "Zorza polarna",
            "ro/index.html": "Aurora boreală",
        },
    },
    "storforsen": {
        "url": "https://www.visitalvsbyn.se/en/upplevelser/storforsen/",
        "display": "visitalvsbyn.se →",
        "h3": {
            "index.html":    "Storforsen rapids",
            "sv/index.html": "Storforsen",
            "fr/index.html": "Rapides de Storforsen",
            "de/index.html": "Stromschnellen Storforsen",
            "pl/index.html": "Bystrza Storforsen",
            "ro/index.html": "Repezișurile Storforsen",
        },
    },
    "lindbacksstadion": {
        "url": "https://www.pitea.se/Upplev/se/produkt/?lang=sv&TLp=1127856",
        "display": "pitea.se →",
        "h3": {
            "index.html":    "Lindbäcksstadion",
            "sv/index.html": "Lindbäcksstadion",
            "fr/index.html": "Lindbäcksstadion",
            "de/index.html": "Lindbäcksstadion",
            "pl/index.html": "Lindbäcksstadion",
            "ro/index.html": "Lindbäcksstadion",
        },
    },
    # --- Practical info ---
    "groceries_ojebyn": {
        "url": "https://www.ica.se/butiker/supermarket/pitea/ica-supermarket-ojebyn-1003700/",
        "display": "ica.se →",
        "h3": {
            "index.html":    "Groceries — Öjebyn",
            "sv/index.html": "Mat — Öjebyn",
            "fr/index.html": "Courses — Öjebyn",
            "de/index.html": "Lebensmittel — Öjebyn",
            "pl/index.html": "Sklepy spożywcze — Öjebyn",
            "ro/index.html": "Cumpărături — Öjebyn",
        },
    },
    "stora_coop": {
        "url": "https://www.coop.se/butiker-erbjudanden/stora-coop/stora-coop-pitea/",
        "display": "coop.se →",
        "h3": {
            "index.html":    "Bigger grocery (5 km)",
            "sv/index.html": "Större mataffär (5 km)",
            "fr/index.html": "Plus grande épicerie (5 km)",
            "de/index.html": "Größerer Supermarkt (5 km)",
            "pl/index.html": "Większy supermarket (5 km)",
            "ro/index.html": "Magazin mai mare (5 km)",
        },
    },
    "systembolaget": {
        "url": "https://www.systembolaget.se/butiker-ombud/butik/norrbottens-lan/pitea/storgatan-65-2504/",
        "display": "systembolaget.se →",
        "h3": {
            "index.html":    "Alcohol — Systembolaget",
            "sv/index.html": "Alkohol — Systembolaget",
            "fr/index.html": "Alcool — Systembolaget",
            "de/index.html": "Alkohol — Systembolaget",
            "pl/index.html": "Alkohol — Systembolaget",
            "ro/index.html": "Alcool — Systembolaget",
        },
    },
    "kifas": {
        "url": "https://www.facebook.com/www.kifas.se",
        "display": "Kifas Pizzeria →",
        "h3": {
            "index.html":    "Eat in Öjebyn",
            "sv/index.html": "Äta i Öjebyn",
            "fr/index.html": "Manger à Öjebyn",
            "de/index.html": "Essen in Öjebyn",
            "pl/index.html": "Jeść w Öjebyn",
            "ro/index.html": "Mâncare în Öjebyn",
        },
    },
    "bishops_arms": {
        "url": "https://www.bishopsarms.com/vara-pubar/pitea/",
        "display": "bishopsarms.com →",
        "h3": {
            "index.html":    "Pubs &amp; bars in Piteå",
            "sv/index.html": "Pubar &amp; barer i Piteå",
            "fr/index.html": "Pubs &amp; bars à Piteå",
            "de/index.html": "Pubs &amp; Bars in Piteå",
            "pl/index.html": "Puby &amp; bary w Piteå",
            "ro/index.html": "Puburi &amp; baruri în Piteå",
        },
    },
    "apotek_hjartat": {
        "url": "https://www.apotekhjartat.se/hitta-apotek-hjartat/apotek-hjartat-vardcentralen-ojebyn/",
        "display": "apotekhjartat.se →",
        "h3": {
            "index.html":    "Pharmacy &amp; healthcare",
            "sv/index.html": "Apotek &amp; vård",
            "fr/index.html": "Pharmacie &amp; santé",
            "de/index.html": "Apotheke &amp; Gesundheit",
            "pl/index.html": "Apteka &amp; opieka zdrowotna",
            "ro/index.html": "Farmacie &amp; sănătate",
        },
    },
}

# Pattern: from <h3>HEADER</h3> to the next \n            </div> (card close)
# The 12-space indent on </div> identifies the card-level closer (vs nested divs).
def make_card_pattern(h3_text: str) -> re.Pattern:
    escaped = re.escape(h3_text)
    return re.compile(
        rf"(<h3>{escaped}</h3>.*?)(\n            </div>)",
        re.DOTALL,
    )


def insert_link(card_html: str, url: str, display: str) -> str:
    # Skip if outbound link already exists in this card
    if 'class="outbound"' in card_html:
        return card_html
    link_html = (
        f'\n                <a class="outbound" href="{url}" '
        f'target="_blank" rel="noopener">{display}</a>'
    )
    return card_html + link_html


def main():
    files = ["index.html", "sv/index.html", "fr/index.html",
             "de/index.html", "pl/index.html", "ro/index.html"]
    for fname in files:
        path = REPO / fname
        text = path.read_text(encoding="utf-8")
        before = text
        added_count = 0
        for card_id, cfg in LINKS.items():
            h3 = cfg["h3"].get(fname)
            if not h3:
                continue
            pattern = make_card_pattern(h3)
            match = pattern.search(text)
            if not match:
                print(f"  {fname}: SKIP {card_id} — h3 '{h3}' not found")
                continue
            card_body = match.group(1)
            closer = match.group(2)
            new_body = insert_link(card_body, cfg["url"], cfg["display"])
            if new_body == card_body:
                # Already had an outbound link — idempotent skip
                continue
            text = text[:match.start()] + new_body + closer + text[match.end():]
            added_count += 1
        if text != before:
            path.write_text(text, encoding="utf-8")
            print(f"✅ {fname}: added {added_count} outbound links")
        else:
            print(f"   {fname}: no changes (already has all links)")


if __name__ == "__main__":
    main()
