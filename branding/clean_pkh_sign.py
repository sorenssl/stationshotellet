"""One-off cleanup: paint over the PKH lightbox sign on the right building
with a copy of the clean red wood wall immediately next to it. Output goes
to images/full/exterior_winter_clean.jpg, which is then used as the source
for cover_photo_generator.py.

Strategy:
  1. Identify the sign bounding box in source pixels (manually measured).
  2. Sample a same-size DONOR region from clean wall to the right of the sign.
  3. Paste donor onto sign location.
  4. Feather the edges with a soft alpha mask so the seam doesn't show.

This is NOT AI inpainting; it's a copy-paste with edge blending. Works because
the right building's wall to the right of the sign is the same red wood at the
same height/lighting. If the result has a visible seam, switch to Cleanup.pictures
for proper AI fill.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "full" / "exterior_winter.jpg"
OUT = ROOT / "images" / "full" / "exterior_winter_clean.jpg"

# PKH sign bounding box in source-pixel coordinates (3968x2976 source).
# Identified by inspecting a high-res crop of the right building.
SIGN_BOX = (2160, 920, 2620, 1070)  # left, top, right, bottom — 460x150 pixels

# Donor strip: thin column of clean red wood wall immediately right of the sign.
# Will be tiled horizontally to cover the full sign width. Same Y range so
# lighting / shadows match the sign's location exactly.
DONOR_STRIP = (2625, 920, 2700, 1070)  # 75x150 clean wall column

# Edge-feather radius (pixels). Softens the seam between patch and untouched wall.
FEATHER_RADIUS = 8


def make_feather_mask(size: tuple[int, int], radius: int) -> Image.Image:
    """White rectangle with feathered (Gaussian-blurred) edges."""
    w, h = size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    inset = radius
    draw.rectangle([(inset, inset), (w - inset, h - inset)], fill=255)
    return mask.filter(ImageFilter.GaussianBlur(radius=radius / 2))


def build_tiled_patch(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Sample DONOR_STRIP and horizontally tile it to fill target_w x target_h.
    Wood paneling is typically horizontal planks, so horizontal tiling preserves
    the natural pattern (same horizontal lines repeat across)."""
    strip = img.crop(DONOR_STRIP)
    sw, sh = strip.size
    if sh != target_h:
        # Resize strip vertically if heights don't match (shouldn't happen if Y aligned)
        strip = strip.resize((sw, target_h), Image.LANCZOS)
        sh = target_h
    canvas = Image.new("RGB", (target_w, target_h))
    x = 0
    flip = False
    while x < target_w:
        # Alternate flipping the strip to break up obvious tiling pattern
        piece = strip.transpose(Image.FLIP_LEFT_RIGHT) if flip else strip
        canvas.paste(piece, (x, 0))
        x += sw
        flip = not flip
    return canvas


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: source not found: {SRC}")
        return 1

    img = Image.open(SRC).convert("RGB")
    print(f"Source: {img.size}")

    sw = SIGN_BOX[2] - SIGN_BOX[0]
    sh = SIGN_BOX[3] - SIGN_BOX[1]
    print(f"Sign region : {SIGN_BOX}  ({sw}x{sh})")
    print(f"Donor strip : {DONOR_STRIP}  ({DONOR_STRIP[2]-DONOR_STRIP[0]}x{DONOR_STRIP[3]-DONOR_STRIP[1]})")

    patch = build_tiled_patch(img, sw, sh)
    mask = make_feather_mask((sw, sh), FEATHER_RADIUS)
    img.paste(patch, (SIGN_BOX[0], SIGN_BOX[1]), mask)

    img.save(OUT, "JPEG", quality=95, optimize=True, progressive=True)
    print(f"Wrote: {OUT}  ({OUT.stat().st_size/1024:.0f} KiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
