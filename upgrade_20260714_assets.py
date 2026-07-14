"""Asset generation for the 2026-07-14 tourist-SEO + style upgrade.

Creates (all tracked by git, originals untouched):
  /favicon.ico                     16+32+48 multi-size, from branding/logos/logo_mark_256.png
  /favicon-32x32.png               32x32
  /apple-touch-icon.png            180x180
  /images/brand/logo-256.png       square SH mark for JSON-LD "logo"
  /images/full/exterior-aurora.jpg + .webp   1600px hero/slideshow (real aurora over our street)
  /images/og-image-aurora.jpg      1200x630 social share card (branded cover, SH badge kept)
  /images/full/entrance-veranda.jpg + .webp  1600px, from untracked Airbnb_Entre.jpg
  /images/thumb/entrance-veranda.jpg + .webp gallery thumb, width matched to existing thumbs

Usage: python upgrade_20260714_assets.py   (run from repo root)
Idempotent — re-running regenerates the same outputs.
"""
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parent
FULL = REPO / "images" / "full"
THUMB = REPO / "images" / "thumb"
BRAND = REPO / "images" / "brand"
LOGOS = REPO / "branding" / "logos"
COVERS = REPO / "branding" / "covers"

WEBP_QUALITY = 82
JPEG_QUALITY = 85


def report(path: Path):
    print(f"  {path.relative_to(REPO)}  ({path.stat().st_size:,} bytes)")


def make_favicons():
    src = Image.open(LOGOS / "logo_mark_256.png").convert("RGB")
    ico = REPO / "favicon.ico"
    src.save(ico, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    report(ico)

    png32 = REPO / "favicon-32x32.png"
    src.resize((32, 32), Image.Resampling.LANCZOS).save(png32, "png", optimize=True)
    report(png32)

    apple = REPO / "apple-touch-icon.png"
    src.resize((180, 180), Image.Resampling.LANCZOS).save(apple, "png", optimize=True)
    report(apple)

    BRAND.mkdir(parents=True, exist_ok=True)
    logo = BRAND / "logo-256.png"
    src.save(logo, "png", optimize=True)
    report(logo)


def resize_to_width(img: Image.Image, width: int) -> Image.Image:
    if img.width <= width:
        return img
    ratio = width / img.width
    return img.resize((width, int(img.height * ratio)), Image.Resampling.LANCZOS)


def save_jpg_webp(img: Image.Image, jpg_path: Path):
    img.save(jpg_path, "jpeg", quality=JPEG_QUALITY, optimize=True, progressive=True)
    report(jpg_path)
    webp_path = jpg_path.with_suffix(".webp")
    img.save(webp_path, "webp", quality=WEBP_QUALITY, method=6)
    report(webp_path)


def make_aurora_hero():
    src = Image.open(COVERS / "cover_plain_exterior_aurora_rotated_1920.jpg").convert("RGB")
    save_jpg_webp(resize_to_width(src, 1600), FULL / "exterior-aurora.jpg")


def make_og_image():
    # Branded cover (SH badge bottom-right). 1920x1080 -> scale to 1200x675,
    # crop 45px off the TOP so the badge and horizon stay in frame -> 1200x630.
    src = Image.open(COVERS / "cover_branded_exterior_aurora_rotated_1920.jpg").convert("RGB")
    scaled = src.resize((1200, int(src.height * 1200 / src.width)), Image.Resampling.LANCZOS)
    if scaled.height < 630:
        raise SystemExit(f"og source too short after scale: {scaled.size}")
    top = scaled.height - 630
    cropped = scaled.crop((0, top, 1200, scaled.height))
    out = REPO / "images" / "og-image-aurora.jpg"
    cropped.save(out, "jpeg", quality=JPEG_QUALITY, optimize=True, progressive=True)
    report(out)
    assert cropped.size == (1200, 630), cropped.size


def make_entrance():
    src_path = FULL / "Airbnb_Entre.jpg"
    if not src_path.exists():
        print("  SKIP entrance: Airbnb_Entre.jpg not found")
        return
    src = Image.open(src_path).convert("RGB")
    save_jpg_webp(resize_to_width(src, 1600), FULL / "entrance-veranda.jpg")

    # Match existing thumbnail width so gallery grid stays consistent
    ref = Image.open(THUMB / "living-room.jpg")
    thumb_w = ref.width
    print(f"  (thumb width matched to living-room.jpg: {thumb_w}px)")
    save_jpg_webp(resize_to_width(src, thumb_w), THUMB / "entrance-veranda.jpg")


def main():
    print("=== favicons + brand logo ===")
    make_favicons()
    print("=== aurora hero (plain cover, 1600px) ===")
    make_aurora_hero()
    print("=== og:image 1200x630 (branded cover) ===")
    make_og_image()
    print("=== entrance photo (full + thumb) ===")
    make_entrance()
    print("DONE")


if __name__ == "__main__":
    main()
