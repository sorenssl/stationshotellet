"""Add 'Guest reviews' section + Self check-in lockbox row + Languages-spoken row.

Four idempotent operations per file:
1. CSS: insert review-card styling before </style> (only if exactly one <style> block)
2. Lockbox row: insert before the payment booking-detail row (anchor = credit-card emoji)
3. Languages-spoken row: insert before payment row (lands between lockbox and payment)
4. Reviews section: insert before <section id="location">

Reviews are quoted in their displayed Airbnb language (verbatim, no translation).
Per-language config below provides translated section title / subtitle / footer link / lockbox row.

Idempotent: each step checks for marker text before inserting. Re-run is safe.

Run from repo root:
    python add_reviews_and_lockbox.py
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent

AIRBNB_URL = "https://www.airbnb.com/h/big-apartment-free-parking-6-beds-host-soren-doushka"
TOTAL_REVIEWS = 63

# Reviews — verbatim from Airbnb listing 22358359, kept in displayed language
REVIEWS = [
    {
        "name": "Amanda", "date": "09/2025",
        "text": "Incredibly nice accommodation, you can tell that they have spent time making it comfortable, clean and homey. The kitchen was super and well-equipped, the bathroom spacious and clean, the bedrooms were cleaned and very comfortable bed. Helpful and nice hosts. Would definitely stay here again.",
    },
    {
        "name": "Deepthi", "date": "12/2024",
        "text": "Soren &amp; Doushka&rsquo;s place was one of the cleanest, most well maintained and well cared for apartments. The place looked exactly like the pictures. The bed was large and comfortable. Soren and Doushka kindly invited us for a traditional Swedish Fika one evening. We started off as hosts and guests but ended up as new friends in an evening full of laughter and connection. Will definitely return to their place when in Pite&aring; next!",
    },
    {
        "name": "Andreas", "date": "01/2025",
        "text": "Wir wollten zum Jahreswechsel ein paar ruhige Tage im skandinavischen Winter verbringen &mdash; au&szlig;en sehr kalt und innen warm und gem&uuml;tlich. Genauso war es! Das Apartment von Doushka und S&ouml;ren war sehr gro&szlig;, perfekt eingerichtet und kuschelig warm. Die Wohnung liegt sehr ruhig, aber die n&auml;chsten Superm&auml;rkte sind zu Fu&szlig; erreichbar. Wir k&ouml;nnen diese Wohnung sehr empfehlen f&uuml;r einen entspannten Urlaub!",
    },
    {
        "name": "John", "date": "08/2025",
        "text": "Felt like home in a safe, quiet area. Highly recommended, excellent hosts, would like to stay here again soon.",
    },
    {
        "name": "Pernilla", "date": "08/2025",
        "text": "Cozy, clean accommodation with the right location for the purpose. Recommended, we will certainly come back.",
    },
    {
        "name": "Biret", "date": "07/2025",
        "text": "Amazing hosts. The apartment was so cozy and nice. Very clean and extra plus with air conditioning. We felt at home and would be happy to come back.",
    },
]

LANGS = {
    "index.html": {
        "label": "Guest reviews",
        "title": "What our guests say",
        "subtitle": "&#9733;&#9733;&#9733;&#9733;&#9733; 63 reviews on Airbnb &mdash; every stay rated 5 stars.",
        "meta_suffix": "Verified Airbnb stay",
        "footer": "Read all 63 reviews on Airbnb &rarr;",
        "lockbox_title": "Self check-in",
        "lockbox_text": "Lockbox at the door &mdash; arrive any time. Code sent by email before arrival.",
        "speak_title": "Languages spoken",
        "speak_text": "Danish, English, French, Norwegian, Swedish.",
    },
    "sv/index.html": {
        "label": "G&auml;stomd&ouml;men",
        "title": "Vad v&aring;ra g&auml;ster s&auml;ger",
        "subtitle": "&#9733;&#9733;&#9733;&#9733;&#9733; 63 omd&ouml;men p&aring; Airbnb &mdash; varje g&auml;st gav 5 av 5 stj&auml;rnor.",
        "meta_suffix": "Verifierad Airbnb-vistelse",
        "footer": "L&auml;s alla 63 omd&ouml;men p&aring; Airbnb &rarr;",
        "lockbox_title": "Sj&auml;lvincheckning",
        "lockbox_text": "Nyckelsk&aring;p vid d&ouml;rren &mdash; kom n&auml;r du vill. Kod skickas via e-post f&ouml;re ankomst.",
        "speak_title": "Spr&aring;k vi talar",
        "speak_text": "Danska, engelska, franska, norska, svenska.",
    },
    "fr/index.html": {
        "label": "Avis voyageurs",
        "title": "Ce que disent nos invit&eacute;s",
        "subtitle": "&#9733;&#9733;&#9733;&#9733;&#9733; 63 avis sur Airbnb &mdash; chaque s&eacute;jour not&eacute; 5 &eacute;toiles.",
        "meta_suffix": "S&eacute;jour Airbnb v&eacute;rifi&eacute;",
        "footer": "Lire les 63 avis sur Airbnb &rarr;",
        "lockbox_title": "Auto-enregistrement",
        "lockbox_text": "Bo&icirc;te &agrave; cl&eacute;s &agrave; la porte &mdash; arrivez &agrave; toute heure. Code envoy&eacute; par e-mail avant l&rsquo;arriv&eacute;e.",
        "speak_title": "Langues parl&eacute;es",
        "speak_text": "Danois, anglais, fran&ccedil;ais, norv&eacute;gien, su&eacute;dois.",
    },
    "de/index.html": {
        "label": "G&auml;stebewertungen",
        "title": "Was unsere G&auml;ste sagen",
        "subtitle": "&#9733;&#9733;&#9733;&#9733;&#9733; 63 Bewertungen auf Airbnb &mdash; jeder Aufenthalt mit 5 Sternen.",
        "meta_suffix": "Verifizierter Airbnb-Aufenthalt",
        "footer": "Alle 63 Bewertungen auf Airbnb lesen &rarr;",
        "lockbox_title": "Selbstanreise",
        "lockbox_text": "Schl&uuml;sselsafe an der T&uuml;r &mdash; Ankunft jederzeit m&ouml;glich. Code wird vor der Anreise per E-Mail gesendet.",
        "speak_title": "Sprachen",
        "speak_text": "D&auml;nisch, Englisch, Franz&ouml;sisch, Norwegisch, Schwedisch.",
    },
    "pl/index.html": {
        "label": "Opinie go&#347;ci",
        "title": "Co m&oacute;wi&#261; nasi go&#347;cie",
        "subtitle": "&#9733;&#9733;&#9733;&#9733;&#9733; 63 opinie na Airbnb &mdash; ka&#380;dy pobyt z 5 gwiazdkami.",
        "meta_suffix": "Zweryfikowany pobyt Airbnb",
        "footer": "Przeczytaj wszystkie 63 opinie na Airbnb &rarr;",
        "lockbox_title": "Samodzielne zameldowanie",
        "lockbox_text": "Skrytka z kluczem przy drzwiach &mdash; przyjed&#378; o dowolnej porze. Kod wysy&#322;any e-mailem przed przyjazdem.",
        "speak_title": "J&#281;zyki",
        "speak_text": "Du&#324;ski, angielski, francuski, norweski, szwedzki.",
    },
    "ro/index.html": {
        "label": "Recenzii oaspe&#539;i",
        "title": "Ce spun oaspe&#539;ii no&#537;tri",
        "subtitle": "&#9733;&#9733;&#9733;&#9733;&#9733; 63 de recenzii pe Airbnb &mdash; fiecare cu 5 stele.",
        "meta_suffix": "Sejur Airbnb verificat",
        "footer": "Cite&#537;te toate cele 63 de recenzii pe Airbnb &rarr;",
        "lockbox_title": "Self check-in",
        "lockbox_text": "Cutie cu cheie la u&#537;&#259; &mdash; sose&#537;te la orice or&#259;. Codul este trimis prin e-mail &icirc;nainte de sosire.",
        "speak_title": "Limbi vorbite",
        "speak_text": "Danez&#259;, englez&#259;, francez&#259;, norvegian&#259;, suedez&#259;.",
    },
}

NEW_CSS = """
        /* Reviews section */
        #reviews {
            background: var(--color-warm);
            padding: 5rem 0;
        }
        .reviews-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 2.5rem;
        }
        .review-card {
            background: var(--color-card);
            padding: 1.6rem;
            border-radius: 10px;
            border: 1px solid var(--color-border);
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            display: flex;
            flex-direction: column;
        }
        .review-stars {
            color: var(--color-accent);
            letter-spacing: 0.18em;
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }
        .review-text {
            font-style: italic;
            line-height: 1.6;
            color: var(--color-text);
            margin: 0 0 1rem;
            font-size: 0.93rem;
            flex-grow: 1;
        }
        .review-meta {
            font-size: 0.82rem;
            color: var(--color-muted);
            margin: 0;
            padding-top: 0.7rem;
            border-top: 1px solid var(--color-border);
        }
        .reviews-footer {
            text-align: center;
            margin-top: 2.5rem;
        }
        .reviews-footer a {
            color: var(--color-accent);
            text-decoration: none;
            font-size: 1rem;
            font-weight: 500;
        }
        .reviews-footer a:hover {
            color: var(--color-accent-hover);
            text-decoration: underline;
        }
"""


def build_reviews_section(cfg: dict) -> str:
    cards = []
    for r in REVIEWS:
        cards.append(
            '            <article class="review-card">\n'
            '                <div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>\n'
            f'                <p class="review-text">&ldquo;{r["text"]}&rdquo;</p>\n'
            f'                <p class="review-meta">&mdash; {r["name"]} &middot; {r["date"]} &middot; {cfg["meta_suffix"]}</p>\n'
            '            </article>'
        )
    cards_html = "\n".join(cards)
    return (
        '<!-- Guest reviews -->\n'
        '<section id="reviews">\n'
        '    <div class="section-inner">\n'
        f'        <span class="section-label">{cfg["label"]}</span>\n'
        f'        <h2 class="section-title">{cfg["title"]}</h2>\n'
        f'        <p class="section-subtitle">{cfg["subtitle"]}</p>\n'
        '        <div class="reviews-grid">\n'
        f'{cards_html}\n'
        '        </div>\n'
        '        <p class="reviews-footer">\n'
        f'            <a class="outbound" href="{AIRBNB_URL}" target="_blank" rel="noopener">{cfg["footer"]}</a>\n'
        '        </p>\n'
        '    </div>\n'
        '</section>\n\n'
    )


def build_lockbox_row(cfg: dict) -> str:
    """Lockbox row matching existing .booking-detail markup. No leading whitespace
    (that's preserved from the file); ends with newline + 16 spaces so the next
    sibling row aligns correctly."""
    return (
        '<div class="booking-detail">\n'
        '                    <span class="booking-detail-icon">&#128273;</span>\n'
        '                    <div class="booking-detail-text">\n'
        f'                        <strong>{cfg["lockbox_title"]}</strong>\n'
        f'                        <span>{cfg["lockbox_text"]}</span>\n'
        '                    </div>\n'
        '                </div>\n'
        '                '
    )


def build_speak_row(cfg: dict) -> str:
    """Languages-spoken booking-detail row. Same structural pattern as lockbox."""
    return (
        '<div class="booking-detail">\n'
        '                    <span class="booking-detail-icon">&#128172;</span>\n'
        '                    <div class="booking-detail-text">\n'
        f'                        <strong>{cfg["speak_title"]}</strong>\n'
        f'                        <span>{cfg["speak_text"]}</span>\n'
        '                    </div>\n'
        '                </div>\n'
        '                '
    )


PAYMENT_ANCHOR = '<div class="booking-detail">\n                    <span class="booking-detail-icon">&#128179;</span>'
LOCATION_ANCHOR = '<section id="location">'
STYLE_CLOSE = '</style>'


def process(path: Path, key: str) -> dict:
    text = path.read_text(encoding="utf-8")
    cfg = LANGS[key]
    before = text
    ops = []

    # 1) CSS injection — only if exactly one <style> block, and review-card not already there
    if ".review-card {" in text:
        ops.append("css-skip")
    else:
        n = text.count(STYLE_CLOSE)
        if n == 1:
            text = text.replace(STYLE_CLOSE, NEW_CSS + "    " + STYLE_CLOSE, 1)
            ops.append("css")
        else:
            ops.append(f"!css-aborted-{n}-style-tags")

    # 2) Lockbox row — insert before payment row.
    # Marker: <strong>title</strong> in the visible row (avoids false-match on JSON-LD).
    if f'<strong>{cfg["lockbox_title"]}</strong>' in text:
        ops.append("lockbox-skip")
    elif PAYMENT_ANCHOR in text:
        text = text.replace(PAYMENT_ANCHOR, build_lockbox_row(cfg) + PAYMENT_ANCHOR, 1)
        ops.append("lockbox")
    else:
        ops.append("!lockbox-anchor-missing")

    # 3) Languages-spoken row — insert before payment row (lands AFTER lockbox)
    if f'<strong>{cfg["speak_title"]}</strong>' in text:
        ops.append("speak-skip")
    elif PAYMENT_ANCHOR in text:
        text = text.replace(PAYMENT_ANCHOR, build_speak_row(cfg) + PAYMENT_ANCHOR, 1)
        ops.append("speak")
    else:
        ops.append("!speak-anchor-missing")

    # 4) Reviews section — insert before <section id="location">
    if 'id="reviews"' in text:
        ops.append("reviews-skip")
    elif LOCATION_ANCHOR in text:
        text = text.replace(LOCATION_ANCHOR, build_reviews_section(cfg) + LOCATION_ANCHOR, 1)
        ops.append("reviews")
    else:
        ops.append("!reviews-anchor-missing")

    if text != before:
        path.write_text(text, encoding="utf-8")
        return {"file": key, "changed": True, "ops": ops}
    return {"file": key, "changed": False, "ops": ops}


def main():
    print("=" * 78)
    for key in LANGS:
        result = process(REPO / key, key)
        marker = "OK " if result["changed"] else "-- "
        ops = ", ".join(result["ops"])
        print(f"{marker} {result['file']:25s} -> {ops}")
    print("=" * 78)


if __name__ == "__main__":
    main()
