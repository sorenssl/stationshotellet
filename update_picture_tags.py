"""Wraps every <img> tag pointing at /images/{full,thumb}/X.jpg with a
<picture> element that prefers WebP and falls back to JPEG.

Also handles the hosts.png → hosts.jpg / hosts.webp swap (cleaner than
keeping a 434 KB PNG referenced in HTML).

Updates the hero CSS background-image to add image-set() with WebP first.

Run from repo root: python update_picture_tags.py

Idempotent — running twice is a no-op (it skips already-wrapped imgs).
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent
HTML_FILES = [
    REPO / "index.html",
    REPO / "sv" / "index.html",
    REPO / "fr" / "index.html",
    REPO / "de" / "index.html",
    REPO / "pl" / "index.html",
    REPO / "ro" / "index.html",
]

# Match a standalone <img ... src="/images/{full,thumb}/X.jpg" ... > NOT already inside <picture>
# We assume each image tag is on a single line (which is the case in this codebase).
IMG_RE = re.compile(
    r'(?P<indent>[ \t]*)<img\s+src="(?P<path>/images/(?:full|thumb)/(?P<basename>[^"]+?))\.jpg"(?P<rest>[^>]*)>'
)

# Special case: hosts.png reference
HOSTS_PNG_RE = re.compile(
    r'(?P<indent>[ \t]*)<img\s+src="/images/thumb/hosts\.png"(?P<rest>[^>]*)>'
)


def wrap_with_picture(match: re.Match) -> str:
    indent = match.group("indent")
    path = match.group("path")
    rest = match.group("rest")
    return (
        f"{indent}<picture>\n"
        f'{indent}    <source srcset="{path}.webp" type="image/webp">\n'
        f'{indent}    <img src="{path}.jpg"{rest}>\n'
        f"{indent}</picture>"
    )


def wrap_hosts(match: re.Match) -> str:
    indent = match.group("indent")
    rest = match.group("rest")
    return (
        f"{indent}<picture>\n"
        f'{indent}    <source srcset="/images/thumb/hosts.webp" type="image/webp">\n'
        f'{indent}    <img src="/images/thumb/hosts.jpg"{rest}>\n'
        f"{indent}</picture>"
    )


# Hero CSS — add image-set() variant. Search for the exact CSS rule.
HERO_CSS_RE = re.compile(
    r"(background:\s*linear-gradient\([^)]*\),\s*)url\('/images/full/kitchen-dining-wide\.jpg'\)\s*center/cover\s*no-repeat;"
)


def upgrade_hero_css(html: str) -> tuple[str, bool]:
    """Add image-set() WebP override after the existing background rule.
    Returns (new_html, did_change)."""
    original = "background: linear-gradient(rgba(26, 21, 13, 0.55), rgba(44, 36, 22, 0.7)), url('/images/full/kitchen-dining-wide.jpg') center/cover no-repeat;"
    if original not in html:
        return html, False
    if "image-set(" in html and "kitchen-dining-wide.webp" in html:
        return html, False  # already upgraded
    # Add an image-set rule that takes precedence on browsers that support it.
    upgrade = (
        original
        + "\n            background-image: image-set("
        + "url('/images/full/kitchen-dining-wide.webp') type('image/webp') 1x, "
        + "url('/images/full/kitchen-dining-wide.jpg') type('image/jpeg') 1x);"
    )
    return html.replace(original, upgrade), True


def process(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    before = text

    # Skip imgs already inside <picture> — quick-and-dirty: if the whole tag
    # is already preceded by <picture> on the prior line, skip. To detect that
    # we inspect each match's surrounding context.
    def replace_if_not_inside_picture(m: re.Match) -> str:
        # Look backwards in the source from the match start.
        start = m.start()
        prefix = text[max(0, start - 80) : start]
        if "<picture>" in prefix and "</picture>" not in prefix:
            return m.group(0)  # already wrapped
        # Lightbox img has src="" — skip those (no .jpg)
        return wrap_with_picture(m)

    text = IMG_RE.sub(replace_if_not_inside_picture, text)
    text = HOSTS_PNG_RE.sub(wrap_hosts, text)
    text, hero_changed = upgrade_hero_css(text)

    if text != before:
        path.write_text(text, encoding="utf-8", newline="")
        return {
            "file": str(path.relative_to(REPO)),
            "changed": True,
            "img_count": before.count("<img ") - text.count("<img "),  # negative = added imgs (didn't happen)
            "picture_added": text.count("<picture>") - before.count("<picture>"),
            "hero_upgraded": hero_changed,
        }
    return {"file": str(path.relative_to(REPO)), "changed": False}


def main():
    print("=" * 70)
    print("Wrapping <img> tags with <picture> + WebP source")
    print("=" * 70)
    for path in HTML_FILES:
        r = process(path)
        print(f"  {r['file']:25s}  ", end="")
        if not r["changed"]:
            print("(no change — already up to date)")
        else:
            print(
                f"+{r['picture_added']:>2} <picture>  "
                f"hero CSS upgraded={r['hero_upgraded']}"
            )
    print("=" * 70)


if __name__ == "__main__":
    main()
