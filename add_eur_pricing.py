"""Add live SEK→EUR conversion to price cards across all 6 language versions.

Operations per file:
1. Add .price-eur CSS rule (after existing .price-compare)
2. Add EUR-display div after each .price-unit (3 prices per file)
3. Add JS at end of last <script> that fetches frankfurter.app rate,
   caches it 1h in localStorage, and populates each .eur-amount span
4. Append "Cash (SEK or EUR) accepted" to the payment line in the
   booking section (per-language translation)

Idempotent: skips files that already have the eur-amount marker.

Run from repo root: python add_eur_pricing.py
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent

PAYMENT_LINE_REPLACEMENTS = {
    "index.html":    ("Swish: 070-671 81 85 &middot; PayPal accepted",
                      "Swish: 070-671 81 85 &middot; PayPal &middot; Cash (SEK or EUR) accepted"),
    "sv/index.html": ("Swish: 070-671 81 85 &middot; PayPal accepteras",
                      "Swish: 070-671 81 85 &middot; PayPal &middot; Kontant (SEK eller EUR) accepteras"),
    "fr/index.html": ("Swish : 070-671 81 85 &middot; PayPal accepté",
                      "Swish : 070-671 81 85 &middot; PayPal &middot; Espèces (SEK ou EUR) acceptés"),
    "de/index.html": ("Swish: 070-671 81 85 &middot; PayPal akzeptiert",
                      "Swish: 070-671 81 85 &middot; PayPal &middot; Bargeld (SEK oder EUR) akzeptiert"),
    "pl/index.html": ("Swish: 070-671 81 85 &middot; PayPal akceptowany",
                      "Swish: 070-671 81 85 &middot; PayPal &middot; Gotówka (SEK lub EUR) akceptowana"),
    "ro/index.html": ("Swish: 070-671 81 85 &middot; PayPal acceptat",
                      "Swish: 070-671 81 85 &middot; PayPal &middot; Numerar (SEK sau EUR) acceptat"),
}

CSS_INSERT_ANCHOR = """        .price-compare {
            text-align: center;
            color: var(--color-accent, #8b6f47);
            margin-top: 0.5rem;
            font-size: 0.88rem;
            font-style: italic;
            opacity: 0.85;
        }"""

CSS_NEW_BLOCK = CSS_INSERT_ANCHOR + """

        .price-eur {
            color: var(--color-muted);
            font-size: 0.82rem;
            margin-top: 0.15rem;
            opacity: 0.85;
            min-height: 1em;
        }"""

# Map price tier (kr value) to its expected unit-line content.
# We need to insert <div class="price-eur" data-sek="X">≈ €<span class="eur-amount">…</span></div>
# right after each <div class="price-unit">...</div>
PRICE_TIERS = [990, 5500, 14000]

# Regex: match a <div class="price-amount">N kr</div> followed eventually by
# <div class="price-unit">...</div>, capture both, and insert EUR div after.
# The N can be "990" or "5 500" or "14 000".
PRICE_BLOCK_RE = re.compile(
    r'(<div class="price-amount">([\d\s]+)\s*kr</div>\s*'
    r'<div class="price-unit">[^<]*</div>)',
)

JS_INSERT_ANCHOR = "// --- end script ---"  # we append before </script>

JS_BLOCK = """
    /* --- Live SEK → EUR conversion (free ECB-sourced rate via frankfurter.app) --- */
    (function updateEurPrices() {
        var els = document.querySelectorAll('.price-eur');
        if (!els.length) return;

        var CACHE_KEY = 'sh_sek_eur_v1';
        var CACHE_TTL_MS = 3600 * 1000;  // 1 hour
        var rate = null;

        try {
            var cached = JSON.parse(localStorage.getItem(CACHE_KEY) || 'null');
            if (cached && (Date.now() - cached.t) < CACHE_TTL_MS && cached.r > 0) {
                rate = cached.r;
            }
        } catch (e) { /* ignore */ }

        function paint(r) {
            els.forEach(function(el) {
                var sek = parseFloat(el.getAttribute('data-sek'));
                var span = el.querySelector('.eur-amount');
                if (!isNaN(sek) && span) {
                    span.textContent = Math.round(sek * r);
                }
            });
        }

        if (rate) {
            paint(rate);
            return;
        }

        fetch('https://api.frankfurter.app/latest?from=SEK&to=EUR', { cache: 'no-store' })
            .then(function(r) { return r.ok ? r.json() : null; })
            .then(function(data) {
                if (data && data.rates && data.rates.EUR) {
                    var r = data.rates.EUR;
                    try {
                        localStorage.setItem(CACHE_KEY, JSON.stringify({ r: r, t: Date.now() }));
                    } catch (e) { /* ignore quota errors */ }
                    paint(r);
                } else {
                    // API returned but no rate — hide EUR displays
                    els.forEach(function(el) { el.style.display = 'none'; });
                }
            })
            .catch(function() {
                // Network/CORS failure — hide EUR displays silently
                els.forEach(function(el) { el.style.display = 'none'; });
            });
    })();
"""


def process(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    before = text
    changes = []

    # 1) CSS — add .price-eur if not already present
    if ".price-eur {" not in text:
        text = text.replace(CSS_INSERT_ANCHOR, CSS_NEW_BLOCK, 1)
        changes.append("css")

    # 2) Insert EUR display divs after each .price-unit (skip if already present)
    if 'class="price-eur"' not in text:
        def replace_price_block(m):
            block = m.group(1)
            sek_text = m.group(2).replace(" ", "")  # "5 500" -> "5500"
            return (block + '\n                '
                    f'<div class="price-eur" data-sek="{sek_text}">'
                    '≈ €<span class="eur-amount">…</span></div>')
        new_text = PRICE_BLOCK_RE.sub(replace_price_block, text)
        if new_text != text:
            text = new_text
            changes.append(f"price-eur×{len(PRICE_TIERS)}")

    # 3) JS — insert before final </script> if not already present
    js_marker = "Live SEK → EUR conversion"
    if js_marker not in text:
        # Find the LAST </script> in the body and inject before it.
        # Pattern: the last </script> just before </body>.
        # In our files, the last <script>...</script> contains slideshow / form code.
        last_script_end = text.rfind("</script>")
        if last_script_end != -1:
            text = text[:last_script_end] + JS_BLOCK + text[last_script_end:]
            changes.append("js")

    # 4) Payment line — language-specific text replacement
    rel_path = str(path.relative_to(REPO)).replace("\\", "/")
    if rel_path in PAYMENT_LINE_REPLACEMENTS:
        old, new = PAYMENT_LINE_REPLACEMENTS[rel_path]
        if old in text and new not in text:
            text = text.replace(old, new)
            changes.append("payment")

    if text != before:
        path.write_text(text, encoding="utf-8")
        return {"file": rel_path, "changed": True, "changes": changes}
    return {"file": rel_path, "changed": False, "changes": []}


def main():
    files = ["index.html", "sv/index.html", "fr/index.html",
             "de/index.html", "pl/index.html", "ro/index.html"]
    print("=" * 60)
    for fname in files:
        result = process(REPO / fname)
        marker = "✅" if result["changed"] else "  "
        ops = ", ".join(result["changes"]) if result["changes"] else "(no changes)"
        print(f"{marker} {result['file']:25s} → {ops}")
    print("=" * 60)


if __name__ == "__main__":
    main()
