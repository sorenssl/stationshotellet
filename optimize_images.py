"""One-shot image optimizer for Stations Hotellet.

Generates WebP variants alongside JPEGs (no replacement of originals).
Compresses hosts.png to hosts.jpg + hosts.webp.
Generates a smaller hero JPEG + WebP for the CSS background.

Usage: python optimize_images.py

Run from repo root. Idempotent — re-running just regenerates WebP files.
"""
from pathlib import Path
from PIL import Image
import sys

REPO = Path(__file__).resolve().parent
FULL = REPO / "images" / "full"
THUMB = REPO / "images" / "thumb"

WEBP_QUALITY = 82       # ~30% smaller than JPEG with imperceptible quality loss
JPEG_QUALITY_HOSTS = 85  # for hosts.png → hosts.jpg conversion
HERO_MAX_WIDTH = 1600    # hero background — 1600px is enough for 4K screens (covers 50% width)

def convert_to_webp(jpg_path: Path) -> int:
    """Generate .webp alongside the .jpg. Returns saved bytes (positive = win)."""
    webp_path = jpg_path.with_suffix(".webp")
    img = Image.open(jpg_path)
    img.save(webp_path, "webp", quality=WEBP_QUALITY, method=6)
    orig_size = jpg_path.stat().st_size
    webp_size = webp_path.stat().st_size
    saved = orig_size - webp_size
    pct = 100 * saved / orig_size
    print(f"  {jpg_path.name:30s} {orig_size:>7,} → {webp_size:>7,} ({pct:+5.1f}%)  [WebP]")
    return saved


def compress_hosts_png():
    """hosts.png is 434 KB — convert to hosts.jpg + hosts.webp (much smaller)."""
    png = THUMB / "hosts.png"
    if not png.exists():
        print(f"  SKIP: {png} not found")
        return 0, 0
    jpg = THUMB / "hosts.jpg"
    webp = THUMB / "hosts.webp"
    img = Image.open(png).convert("RGB")  # drop alpha — flatten on white
    img.save(jpg, "jpeg", quality=JPEG_QUALITY_HOSTS, optimize=True, progressive=True)
    img.save(webp, "webp", quality=WEBP_QUALITY, method=6)
    orig = png.stat().st_size
    new_jpg = jpg.stat().st_size
    new_webp = webp.stat().st_size
    print(f"  {png.name:30s} {orig:>7,} → JPG {new_jpg:>7,} / WebP {new_webp:>7,}  [PNG→JPG+WebP]")
    return orig - new_jpg, orig - new_webp


def make_hero_smaller():
    """Generate a 1600px-wide hero variant (CSS background only renders ~50% width on most screens)."""
    src = FULL / "kitchen-dining-wide.jpg"
    if not src.exists():
        print(f"  SKIP: {src} not found")
        return 0
    img = Image.open(src)
    if img.width <= HERO_MAX_WIDTH:
        print(f"  hero already <={HERO_MAX_WIDTH}px wide ({img.width}px); skipping resize")
        return 0
    ratio = HERO_MAX_WIDTH / img.width
    new_size = (HERO_MAX_WIDTH, int(img.height * ratio))
    resized = img.resize(new_size, Image.Resampling.LANCZOS)
    out_jpg = FULL / "hero-1600.jpg"
    out_webp = FULL / "hero-1600.webp"
    resized.save(out_jpg, "jpeg", quality=85, optimize=True, progressive=True)
    resized.save(out_webp, "webp", quality=WEBP_QUALITY, method=6)
    orig = src.stat().st_size
    new_jpg = out_jpg.stat().st_size
    new_webp = out_webp.stat().st_size
    print(f"  hero (1600px)                  {orig:>7,} → JPG {new_jpg:>7,} / WebP {new_webp:>7,}")
    return orig - new_webp


def main():
    print("=" * 70)
    print("Stations Hotellet — image optimization pass")
    print("=" * 70)
    total_saved_webp = 0

    print("\n--- /images/full/ — slideshow originals → WebP ---")
    for jpg in sorted(FULL.glob("*.jpg")):
        # skip the resized hero we generate below
        if jpg.name == "hero-1600.jpg":
            continue
        total_saved_webp += convert_to_webp(jpg)

    print("\n--- /images/thumb/ — gallery thumbnails → WebP ---")
    for jpg in sorted(THUMB.glob("*.jpg")):
        if jpg.name == "hosts.jpg":
            continue  # handled by compress_hosts_png
        total_saved_webp += convert_to_webp(jpg)

    print("\n--- hosts.png → hosts.jpg + hosts.webp ---")
    hosts_jpg_saved, hosts_webp_saved = compress_hosts_png()

    print("\n--- Smaller hero image (1600px) ---")
    hero_saved = make_hero_smaller()

    print("\n" + "=" * 70)
    print("Summary (WebP-served path):")
    print(f"  WebP conversions saved:    {total_saved_webp:>9,} bytes")
    print(f"  hosts.png → hosts.webp:    {hosts_webp_saved:>9,} bytes")
    print(f"  hero JPEG → hero-1600.webp: {hero_saved:>9,} bytes")
    grand = total_saved_webp + hosts_webp_saved + hero_saved
    print(f"  TOTAL:                     {grand:>9,} bytes ({grand/1024:.0f} KB)")
    print("=" * 70)


if __name__ == "__main__":
    main()
