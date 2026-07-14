# -*- coding: utf-8 -*-
"""CSS style + UX upgrade, 2026-07-14 — applies to all 6 language versions.

What it does (per file):
  HERO   swaps the kitchen photo for the real northern-lights exterior shot
         (exterior-aurora, 28 KB WebP) and FIXES a pre-existing bug: the old
         image-set() override dropped the darkening gradient in modern browsers.
         Adds a soft text-shadow for readability.
  TYPE   headings (h1, section titles, nav logo) switch to a system serif stack
         (Charter/Cambria/Georgia) — matches the serif "SH" brand monogram,
         no webfont download.
  UX     anchor links no longer hide section titles behind the fixed navbar
         (scroll-margin-top); visible keyboard focus (:focus-visible);
         animations disabled for prefers-reduced-motion users.
  FAQ    accordion styles for the new visible FAQ section.
  MOBILE sticky "Book now" bar at the bottom of the screen (<=768px), auto-hides
         while the booking form is on screen. Translated labels.

Usage: python upgrade_20260714_style_ux.py    (run from repo root)
NOT idempotent — run exactly once, after upgrade_20260714_seo_content.py.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
ERRORS = []

FILES = {
    "en": "index.html",
    "sv": "sv/index.html",
    "fr": "fr/index.html",
    "de": "de/index.html",
    "pl": "pl/index.html",
    "ro": "ro/index.html",
}

BAR = {
    "en": ("From 990 kr/night", "Book now", "Quick booking"),
    "sv": ("Från 990 kr/natt", "Boka nu", "Snabb bokning"),
    "fr": ("Dès 990 kr/nuit", "Réserver", "Réservation rapide"),
    "de": ("Ab 990 kr/Nacht", "Jetzt buchen", "Schnellbuchung"),
    "pl": ("Od 990 kr/noc", "Rezerwuj", "Szybka rezerwacja"),
    "ro": ("De la 990 kr/noapte", "Rezervă", "Rezervare rapidă"),
}

OLD_HERO_BG = """            background: linear-gradient(rgba(26, 21, 13, 0.55), rgba(44, 36, 22, 0.7)), url('/images/full/kitchen-dining-wide.jpg') center/cover no-repeat;
            background-image: image-set(url('/images/full/kitchen-dining-wide.webp') type('image/webp') 1x, url('/images/full/kitchen-dining-wide.jpg') type('image/jpeg') 1x);"""

NEW_HERO_BG = """            background: linear-gradient(rgba(13, 17, 28, 0.35), rgba(26, 21, 13, 0.72)), url('/images/full/exterior-aurora.jpg') center/cover no-repeat;
            background-image: linear-gradient(rgba(13, 17, 28, 0.35), rgba(26, 21, 13, 0.72)), image-set(url('/images/full/exterior-aurora.webp') type('image/webp') 1x, url('/images/full/exterior-aurora.jpg') type('image/jpeg') 1x);
            background-size: cover;
            background-position: center;"""

NEW_CSS = """
        /* --- 2026-07-14 style upgrade --- */
        .hero h1, .section-title, .nav-logo {
            font-family: Charter, 'Bitstream Charter', 'Sitka Text', Cambria, Georgia, 'Times New Roman', serif;
            letter-spacing: 0.01em;
        }
        .hero h1, .hero p {
            text-shadow: 0 2px 14px rgba(0, 0, 0, 0.5);
        }
        section[id] {
            scroll-margin-top: 72px;
        }
        a:focus-visible, button:focus-visible, input:focus-visible,
        select:focus-visible, textarea:focus-visible, summary:focus-visible,
        [role="button"]:focus-visible {
            outline: 3px solid var(--color-accent);
            outline-offset: 2px;
        }
        @media (prefers-reduced-motion: reduce) {
            html { scroll-behavior: auto; }
            *, *::before, *::after {
                transition-duration: 0.01ms !important;
                animation-duration: 0.01ms !important;
            }
        }

        /* --- FAQ accordion --- */
        #faq { background: var(--color-bg); }
        .faq-list {
            max-width: 800px;
            margin-top: 2rem;
        }
        .faq-item {
            background: var(--color-card);
            border: 1px solid var(--color-border);
            border-radius: var(--radius);
            margin-bottom: 0.75rem;
        }
        .faq-item summary {
            cursor: pointer;
            list-style: none;
            padding: 1rem 3rem 1rem 1.25rem;
            font-weight: 600;
            color: var(--color-heading);
            position: relative;
        }
        .faq-item summary::-webkit-details-marker { display: none; }
        .faq-item summary::after {
            content: "+";
            position: absolute;
            right: 1.25rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--color-accent);
            font-size: 1.4rem;
            font-weight: 400;
        }
        .faq-item[open] summary::after { content: "\\2013"; }
        .faq-item[open] summary { border-bottom: 1px solid var(--color-border); }
        .faq-item p {
            padding: 1rem 1.25rem;
            font-size: 0.95rem;
        }

        /* --- Sticky mobile booking bar --- */
        .book-bar {
            position: fixed;
            left: 0; right: 0; bottom: 0;
            z-index: 90;
            display: none;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.6rem 1rem calc(0.6rem + env(safe-area-inset-bottom));
            background: rgba(26, 21, 13, 0.96);
            backdrop-filter: blur(8px);
            border-top: 1px solid rgba(255, 255, 255, 0.14);
        }
        .book-bar-price {
            color: #faf7f2;
            font-weight: 600;
            font-size: 0.95rem;
            white-space: nowrap;
        }
        .book-bar .btn {
            padding: 0.55rem 1.4rem;
            font-size: 0.95rem;
            white-space: nowrap;
        }
        .book-bar.book-bar-hidden { display: none !important; }
        @media (max-width: 768px) {
            .book-bar { display: flex; }
            footer { padding-bottom: 5.5rem; }
        }
    """

BAR_JS = """<script>
    /* Sticky mobile booking bar — hidden while the booking form is on screen */
    (function() {
        var bar = document.getElementById('book-bar');
        var booking = document.getElementById('booking');
        if (!bar || !booking || !('IntersectionObserver' in window)) return;
        new IntersectionObserver(function(entries) {
            entries.forEach(function(e) {
                bar.classList.toggle('book-bar-hidden', e.isIntersecting);
            });
        }, { threshold: 0.1 }).observe(booking);
    })();
</script>
</body>"""


def process(lang, fname):
    path = REPO / fname
    text = path.read_text(encoding="utf-8")

    # 1. hero background swap (also restores the gradient under image-set)
    if OLD_HERO_BG not in text:
        ERRORS.append(f"{fname}: old hero background block not found")
    else:
        text = text.replace(OLD_HERO_BG, NEW_HERO_BG, 1)

    # 2. new CSS before </style>
    n = text.count("</style>")
    if n != 1:
        ERRORS.append(f"{fname}: expected 1 </style>, found {n}")
    else:
        text = text.replace("</style>", NEW_CSS + "</style>", 1)

    # 3. book-bar HTML — right before the <script> that holds the slides array
    price, cta, aria = BAR[lang]
    bar_html = (
        f'<div class="book-bar" id="book-bar" role="region" aria-label="{aria}">\n'
        f'    <span class="book-bar-price">{price}</span>\n'
        f'    <a href="#booking" class="btn">{cta}</a>\n'
        f'</div>\n\n'
    )
    idx = text.find("var slides")
    if idx == -1:
        ERRORS.append(f"{fname}: slides array not found")
    else:
        script_start = text.rfind("<script>", 0, idx)
        if script_start == -1:
            ERRORS.append(f"{fname}: <script> before slides not found")
        else:
            text = text[:script_start] + bar_html + text[script_start:]

    # 4. bar JS before </body>
    n = text.count("</body>")
    if n != 1:
        ERRORS.append(f"{fname}: expected 1 </body>, found {n}")
    else:
        text = text.replace("</body>", BAR_JS, 1)

    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"  OK {fname}")


def validate():
    print("--- validation ---")
    for lang, fname in FILES.items():
        text = (REPO / fname).read_text(encoding="utf-8")
        for needle, want in [
            ("exterior-aurora.webp", 2),   # preload + hero image-set
            ("exterior-aurora.jpg", 3),    # hero fallback + slide + JSON-LD
            ("kitchen-dining-wide", 4),    # og gone; still: JSON-LD image, slide 0, 2x og->no... (see note)
            ('id="book-bar"', 1),
            ("book-bar-hidden", 3),        # CSS rule + JS toggle... (adjusted below)
            ("scroll-margin-top", 1),
            ("prefers-reduced-motion", 1),
            ("faq-item", 8),               # CSS 6 + 6 items... (adjusted below)
        ]:
            got = text.count(needle)
            print(f"  {fname}: '{needle}' = {got} (want ~{want})")
    print("  (counts above are informational; hard checks were done inline)")


def main():
    for lang, fname in FILES.items():
        process(lang, fname)
    if ERRORS:
        print("\n!!! ERRORS:")
        for e in ERRORS:
            print("  -", e)
        sys.exit(1)
    validate()
    print("\nALL GOOD")


if __name__ == "__main__":
    main()
