"""Enhance Location section's airport card with Swedavia + car-rental links.

Per-language: replaces the simple "Luleå Airport (LLA), approx. 50 km" line
with extended content including car-rental info + 2 outbound links to:
  - swedavia.{com|se}/lulea/  (airport homepage)
  - swedavia.com/lulea/carrental/  (official rental hub — Avis, Budget,
    Europcar, Hertz, Mabi, National, Sixt all listed there)

Also broadens the .outbound CSS class scope so it works inside
.location-card (was previously scoped to .local-card only).

Run from repo root: python add_airport_links.py
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent

# Old → new airport card paragraph per language.
# The OLD value is the EXACT existing line; NEW replaces it with the
# extended content (still inside the same .location-card div).
CARDS = {
    "index.html": {
        "old": "<p>Luleå Airport (LLA), approx. 50 km</p>",
        "new": (
            "<p>Luleå Airport (LLA), approx. 50 km</p>\n"
            '                <p style="margin-top:0.5rem; font-size:0.88rem;">Direct flights from Stockholm. Car rental at the airport: Avis, Budget, Europcar, Hertz, Mabi, National, Sixt.</p>\n'
            '                <p style="margin-top:0.4rem;"><a class="outbound" href="https://www.swedavia.com/lulea/" target="_blank" rel="noopener">swedavia.com/lulea →</a><br>'
            '<a class="outbound" href="https://www.swedavia.com/lulea/carrental/" target="_blank" rel="noopener">car rental at LLA →</a></p>'
        ),
    },
    "sv/index.html": {
        "old": "<p>Luleå flygplats (LLA), ca 50 km</p>",
        "new": (
            "<p>Luleå flygplats (LLA), ca 50 km</p>\n"
            '                <p style="margin-top:0.5rem; font-size:0.88rem;">Direktflyg från Stockholm. Biluthyrning på flygplatsen: Avis, Budget, Europcar, Hertz, Mabi, National, Sixt.</p>\n'
            '                <p style="margin-top:0.4rem;"><a class="outbound" href="https://www.swedavia.se/lulea/" target="_blank" rel="noopener">swedavia.se/lulea →</a><br>'
            '<a class="outbound" href="https://www.swedavia.com/lulea/carrental/" target="_blank" rel="noopener">biluthyrning på LLA →</a></p>'
        ),
    },
    "fr/index.html": {
        "old": "<p>Aéroport de Luleå (LLA), env. 50 km</p>",
        "new": (
            "<p>Aéroport de Luleå (LLA), env. 50 km</p>\n"
            '                <p style="margin-top:0.5rem; font-size:0.88rem;">Vols directs depuis Stockholm. Location de voiture à l\'aéroport : Avis, Budget, Europcar, Hertz, Mabi, National, Sixt.</p>\n'
            '                <p style="margin-top:0.4rem;"><a class="outbound" href="https://www.swedavia.com/lulea/" target="_blank" rel="noopener">swedavia.com/lulea →</a><br>'
            '<a class="outbound" href="https://www.swedavia.com/lulea/carrental/" target="_blank" rel="noopener">location voiture à LLA →</a></p>'
        ),
    },
    "de/index.html": {
        "old": "<p>Flughafen Luleå (LLA), ca. 50 km</p>",
        "new": (
            "<p>Flughafen Luleå (LLA), ca. 50 km</p>\n"
            '                <p style="margin-top:0.5rem; font-size:0.88rem;">Direktflüge ab Stockholm. Mietwagen am Flughafen: Avis, Budget, Europcar, Hertz, Mabi, National, Sixt.</p>\n'
            '                <p style="margin-top:0.4rem;"><a class="outbound" href="https://www.swedavia.com/lulea/" target="_blank" rel="noopener">swedavia.com/lulea →</a><br>'
            '<a class="outbound" href="https://www.swedavia.com/lulea/carrental/" target="_blank" rel="noopener">Mietwagen am LLA →</a></p>'
        ),
    },
    "pl/index.html": {
        "old": "<p>Lotnisko Luleå (LLA), około 50 km</p>",
        "new": (
            "<p>Lotnisko Luleå (LLA), około 50 km</p>\n"
            '                <p style="margin-top:0.5rem; font-size:0.88rem;">Loty bezpośrednie ze Sztokholmu. Wynajem samochodu na lotnisku: Avis, Budget, Europcar, Hertz, Mabi, National, Sixt.</p>\n'
            '                <p style="margin-top:0.4rem;"><a class="outbound" href="https://www.swedavia.com/lulea/" target="_blank" rel="noopener">swedavia.com/lulea →</a><br>'
            '<a class="outbound" href="https://www.swedavia.com/lulea/carrental/" target="_blank" rel="noopener">wynajem samochodu LLA →</a></p>'
        ),
    },
    "ro/index.html": {
        "old": "<p>Aeroportul Luleå (LLA), aprox. 50 km</p>",
        "new": (
            "<p>Aeroportul Luleå (LLA), aprox. 50 km</p>\n"
            '                <p style="margin-top:0.5rem; font-size:0.88rem;">Zboruri directe din Stockholm. Închiriere de mașini la aeroport: Avis, Budget, Europcar, Hertz, Mabi, National, Sixt.</p>\n'
            '                <p style="margin-top:0.4rem;"><a class="outbound" href="https://www.swedavia.com/lulea/" target="_blank" rel="noopener">swedavia.com/lulea →</a><br>'
            '<a class="outbound" href="https://www.swedavia.com/lulea/carrental/" target="_blank" rel="noopener">închiriere mașini la LLA →</a></p>'
        ),
    },
}

# Broaden .outbound CSS so it works in .location-card too (was scoped to
# .local-card only). Idempotent — script checks if already broadened.
OLD_CSS = """        .local-card a.outbound {
            display: inline-block; margin-top: 0.3rem;
            color: var(--color-accent); text-decoration: none;
            font-size: 0.88rem; font-weight: 500;
        }
        .local-card a.outbound:hover {
            text-decoration: underline; color: var(--color-accent-hover);
        }"""

NEW_CSS = """        .local-card a.outbound,
        .location-card a.outbound {
            display: inline-block; margin-top: 0.3rem;
            color: var(--color-accent); text-decoration: none;
            font-size: 0.88rem; font-weight: 500;
        }
        .local-card a.outbound:hover,
        .location-card a.outbound:hover {
            text-decoration: underline; color: var(--color-accent-hover);
        }"""


def process(path: Path, key: str) -> dict:
    text = path.read_text(encoding="utf-8")
    before = text
    changes = []

    # 1) CSS broadening (idempotent)
    if ".location-card a.outbound" not in text:
        if OLD_CSS in text:
            text = text.replace(OLD_CSS, NEW_CSS, 1)
            changes.append("css")

    # 2) Airport card content (idempotent — skip if links already present)
    cfg = CARDS[key]
    if "swedavia.com/lulea" not in text and cfg["old"] in text:
        text = text.replace(cfg["old"], cfg["new"], 1)
        changes.append("airport-card")

    if text != before:
        path.write_text(text, encoding="utf-8")
        return {"file": key, "changed": True, "ops": changes}
    return {"file": key, "changed": False}


def main():
    print("=" * 60)
    for key in CARDS:
        result = process(REPO / key, key)
        marker = "✅" if result["changed"] else "⏭"
        ops = ", ".join(result["ops"]) if result.get("ops") else "(no change)"
        print(f"{marker} {result['file']:25s} → {ops}")
    print("=" * 60)


if __name__ == "__main__":
    main()
