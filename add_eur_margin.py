"""Add 4% service margin to EUR conversion JS in all 6 language files.

Idempotent: skips files that already have EUR_MARGIN constant.

Run from repo root: python add_eur_margin.py
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent

OLD_CACHE_TTL = """        var CACHE_KEY = 'sh_sek_eur_v1';
        var CACHE_TTL_MS = 3600 * 1000;  // 1 hour
        var rate = null;"""

NEW_CACHE_TTL = """        var CACHE_KEY = 'sh_sek_eur_v1';
        var CACHE_TTL_MS = 3600 * 1000;  // 1 hour
        // EUR cash service margin: covers bank's SEK conversion spread (~1.5-3%)
        // plus a small service buffer. Tune this to taste — 0.04 = 4%.
        var EUR_MARGIN = 0.04;
        var rate = null;"""

OLD_PAINT = """                if (!isNaN(sek) && span) {
                    span.textContent = Math.round(sek * r);
                }"""

NEW_PAINT = """                if (!isNaN(sek) && span) {
                    // Apply service margin so EUR cash payment covers Tony's
                    // SEK conversion costs at the bank.
                    span.textContent = Math.round(sek * r * (1 + EUR_MARGIN));
                }"""


def process(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if "EUR_MARGIN" in text:
        return {"file": str(path.relative_to(REPO)), "changed": False, "reason": "already has margin"}
    new_text = text
    if OLD_CACHE_TTL in new_text:
        new_text = new_text.replace(OLD_CACHE_TTL, NEW_CACHE_TTL, 1)
    if OLD_PAINT in new_text:
        new_text = new_text.replace(OLD_PAINT, NEW_PAINT, 1)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return {"file": str(path.relative_to(REPO)), "changed": True}
    return {"file": str(path.relative_to(REPO)), "changed": False, "reason": "anchors not found"}


def main():
    files = ["index.html", "sv/index.html", "fr/index.html",
             "de/index.html", "pl/index.html", "ro/index.html"]
    for fname in files:
        result = process(REPO / fname)
        marker = "✅" if result["changed"] else "⏭"
        reason = f" ({result.get('reason', '')})" if not result["changed"] else ""
        print(f"{marker} {result['file']}{reason}")


if __name__ == "__main__":
    main()
