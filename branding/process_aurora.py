"""One-off: prepare exterior_aurora.jpg for use as a cover/gallery photo.

Steps:
  1. Apply EXIF rotation (the photo has orientation tag 6 = 90° CW).
  2. Gentle enhancement — auroras over-saturate fast, so very small bumps:
     +6% saturation, +5% contrast, +8% sharpness.
  3. Save rotated+enhanced master as exterior_aurora_rotated.jpg.
  4. Also generate a square-format version for Instagram / GBP square photo slot.

After this, run cover_photo_generator.py on the rotated source for 16:9 covers.
"""
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "full" / "exterior_aurora.jpg"
OUT_ROTATED = ROOT / "images" / "full" / "exterior_aurora_rotated.jpg"
OUT_SQUARE = ROOT / "branding" / "covers" / "aurora_square_1080.jpg"
OUT_SQUARE_LG = ROOT / "branding" / "covers" / "aurora_square_2160.jpg"


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: source not found: {SRC}")
        return 1

    img = Image.open(SRC)
    print(f"Source: {img.size}  EXIF orientation: {img.getexif().get(0x0112, 'none')}")

    img = ImageOps.exif_transpose(img).convert("RGB")
    print(f"After EXIF rotation: {img.size}")

    img = ImageEnhance.Color(img).enhance(1.06)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.08)

    img.save(OUT_ROTATED, "JPEG", quality=95, optimize=True, progressive=True)
    print(f"Wrote: {OUT_ROTATED.name}  ({OUT_ROTATED.stat().st_size/1024:.0f} KiB)")

    OUT_SQUARE.parent.mkdir(exist_ok=True)
    sq_lg = img.resize((2160, 2160), Image.LANCZOS)
    sq_lg.save(OUT_SQUARE_LG, "JPEG", quality=92, optimize=True, progressive=True)
    print(f"Wrote: {OUT_SQUARE_LG.name}  2160x2160  ({OUT_SQUARE_LG.stat().st_size/1024:.0f} KiB)")

    sq = img.resize((1080, 1080), Image.LANCZOS)
    sq.save(OUT_SQUARE, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"Wrote: {OUT_SQUARE.name}  1080x1080  ({OUT_SQUARE.stat().st_size/1024:.0f} KiB)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
