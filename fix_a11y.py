"""Apply WCAG accessibility fixes to all 6 language files.

Three fixes (idempotent):
1. Heading hierarchy: <h4> -> <h3> for all 15 occurrences per file
   (12 amenity categories + 3 location cards). They are direct children
   of <h2> sections, so should be <h3>, not <h4>.
2. Document landmark: wrap main content in <main>...</main>.
   Insert <main> after </nav>, </main> before <footer>.
3. (Color contrast already fixed in a prior step by editing CSS vars
   directly. This script does NOT touch the CSS palette.)

Re-run safe: each step checks for marker text before applying.

Run from repo root:
    python fix_a11y.py
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent

FILES = [
    "index.html", "sv/index.html", "fr/index.html",
    "de/index.html", "pl/index.html", "ro/index.html",
]


def fix_headings(text: str) -> tuple[str, str]:
    """h4 -> h3 across the file. Returns (new_text, op_label)."""
    if "<h4" not in text and "</h4>" not in text:
        return text, "h-skip"
    new_text = text.replace("<h4>", "<h3>").replace("<h4 ", "<h3 ").replace("</h4>", "</h3>")
    return new_text, "headings" if new_text != text else "h-skip"


def fix_amenity_css_selector(text: str) -> tuple[str, str]:
    """Update CSS selector .amenity-category h4 -> h3 to match new HTML."""
    if ".amenity-category h4" not in text:
        return text, "css-skip"
    new_text = text.replace(".amenity-category h4", ".amenity-category h3")
    return new_text, "css"


def add_main_landmark(text: str) -> tuple[str, str]:
    """Wrap content between </nav> and <footer> in <main>...</main>."""
    if "<main>" in text or "</main>" in text:
        return text, "main-skip"
    if "</nav>" not in text or "<footer>" not in text:
        return text, "!main-anchors-missing"
    # Open tag: after </nav>
    new_text = text.replace("</nav>\n", "</nav>\n\n<main>\n", 1)
    # Close tag: before <footer>
    new_text = new_text.replace("<footer>", "</main>\n\n<footer>", 1)
    return new_text, "main"


def process(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    before = text
    ops = []

    text, op1 = fix_headings(text)
    ops.append(op1)

    text, op_css = fix_amenity_css_selector(text)
    ops.append(op_css)

    text, op2 = add_main_landmark(text)
    ops.append(op2)

    if text != before:
        path.write_text(text, encoding="utf-8")
        return {"file": str(path.relative_to(REPO)), "changed": True, "ops": ops}
    return {"file": str(path.relative_to(REPO)), "changed": False, "ops": ops}


def main():
    print("=" * 70)
    print("Accessibility fixes: heading hierarchy + <main> landmark")
    print("=" * 70)
    for f in FILES:
        result = process(REPO / f)
        marker = "OK " if result["changed"] else "-- "
        ops = ", ".join(result["ops"])
        print(f"{marker} {result['file']:25s} -> {ops}")
    print("=" * 70)


if __name__ == "__main__":
    main()
