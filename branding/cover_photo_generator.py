"""Generate Google Business Profile cover photos from existing site images.

Crops a source image to 16:9 (Google's recommended ratio) at multiple sizes.
Produces both:
  - covers/cover_plain_*.jpg    pure photo (most authentic — recommended for GBP)
  - covers/cover_branded_*.jpg  same photo with the mark-only logo in bottom-right

Reads from logo_config.json for branding (uses the same colors/fonts as logos).

Run:
    python cover_photo_generator.py
    python cover_photo_generator.py --source ../images/full/living-room.jpg
    python cover_photo_generator.py --config logo_config_othersite.json --source path/to/photo.jpg
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parent

# 16:9 sizes — GBP cover photo ratio. Listed largest-first.
COVER_SIZES = [
    (2400, 1350),   # high-res future-proof
    (1920, 1080),   # Full HD
    (1024, 575),    # GBP minimum (actually 1024x576 = 16:9, GBP says 575 but 576 is exact)
]


def _hex_to_rgb(value) -> tuple[int, int, int]:
    if isinstance(value, (list, tuple)) and len(value) == 3:
        return tuple(int(c) for c in value)
    s = str(value).lstrip("#")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def _font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for candidate in [name, "georgia.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def apply_enhancement(img: Image.Image, level: str = "moderate") -> Image.Image:
    """Subtle photographic enhancements — designed for outdoor / natural-light shots
    that benefit from slightly punchier color without looking over-processed.

    Levels:
      moderate (default): +12% saturation, +8% contrast, +15% sharpness
      strong:             +20% saturation, +12% contrast, +25% sharpness
    """
    if level == "strong":
        sat, con, shp = 1.20, 1.12, 1.25
    else:
        sat, con, shp = 1.12, 1.08, 1.15
    img = ImageEnhance.Color(img).enhance(sat)
    img = ImageEnhance.Contrast(img).enhance(con)
    img = ImageEnhance.Sharpness(img).enhance(shp)
    return img


def crop_to_16x9(img: Image.Image, horizontal_bias: float = 0.5,
                 vertical_bias: float = 0.5) -> Image.Image:
    """Crop to exactly 16:9 ratio without distortion.

    horizontal_bias / vertical_bias: 0.0 = anchor to left/top, 0.5 = centered (default),
    1.0 = anchor to right/bottom. Use to keep the subject in frame when the photo
    isn't already centered (e.g., subject is in the left third)."""
    w, h = img.size
    target_ratio = 16 / 9
    current_ratio = w / h
    if current_ratio > target_ratio:
        # Too wide — crop sides
        new_w = int(h * target_ratio)
        x_off = int((w - new_w) * horizontal_bias)
        return img.crop((x_off, 0, x_off + new_w, h))
    else:
        # Too tall — crop top + bottom
        new_h = int(w / target_ratio)
        y_off = int((h - new_h) * vertical_bias)
        return img.crop((0, y_off, w, y_off + new_h))


def make_mark_overlay(size: int, cfg: dict) -> Image.Image:
    """Generate a small mark-only logo as a transparent-background PNG layer."""
    bg = _hex_to_rgb(cfg["colors"]["background"]) + (235,)  # near-opaque cream
    accent = _hex_to_rgb(cfg["colors"]["accent"]) + (255,)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle (cream, slightly transparent)
    pad = int(size * 0.02)
    draw.ellipse([(pad, pad), (size - pad, size - pad)], fill=bg)

    # Outer ring
    margin_outer = int(size * 0.05)
    margin_inner = int(size * 0.08)
    draw.ellipse(
        [(margin_outer, margin_outer), (size - margin_outer, size - margin_outer)],
        outline=accent, width=max(2, int(size * 0.012)),
    )
    draw.ellipse(
        [(margin_inner, margin_inner), (size - margin_inner, size - margin_inner)],
        outline=accent, width=max(1, int(size * 0.004)),
    )

    # Initials
    mono_font = _font(cfg["fonts"]["monogram"], int(size * 0.42))
    text = cfg["initials"]
    bbox = draw.textbbox((0, 0), text, font=mono_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1] - int(size * 0.02)
    draw.text((x, y), text, font=mono_font, fill=accent)
    return img


def make_cover(source: Path, out_dir: Path, cfg: dict, enhance: str = "off",
               h_bias: float = 0.5, v_bias: float = 0.5,
               region: tuple[int, int, int, int] | None = None) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Source image not found: {source}")
    src = Image.open(source).convert("RGB")
    print(f"  Source: {source.name}  ({src.size[0]}x{src.size[1]})")
    if region is not None:
        src = src.crop(region)
        print(f"  Pre-crop region: {region}  ->  {src.size[0]}x{src.size[1]}")
    base = crop_to_16x9(src, horizontal_bias=h_bias, vertical_bias=v_bias)
    print(f"  After 16:9 crop: {base.size[0]}x{base.size[1]}  (h_bias={h_bias}, v_bias={v_bias})")
    if enhance != "off":
        base = apply_enhancement(base, level=enhance)
        print(f"  Enhancement applied: {enhance}")

    out_dir.mkdir(exist_ok=True)
    source_stem = source.stem.replace(".", "_")

    for w, h in COVER_SIZES:
        # Plain version
        plain = base.resize((w, h), Image.LANCZOS)
        plain_path = out_dir / f"cover_plain_{source_stem}_{w}.jpg"
        plain.save(plain_path, "JPEG", quality=88, optimize=True, progressive=True)
        print(f"    {plain_path.name:50s}  {w}x{h}  {plain_path.stat().st_size/1024:6.1f} KiB")

        # Branded version: paste mark in bottom-right corner
        branded = plain.copy().convert("RGBA")
        mark_size = int(w * 0.10)  # ~10% of width
        margin = int(w * 0.025)
        mark = make_mark_overlay(mark_size, cfg)
        branded.paste(mark, (w - mark_size - margin, h - mark_size - margin), mark)
        branded_path = out_dir / f"cover_branded_{source_stem}_{w}.jpg"
        branded.convert("RGB").save(branded_path, "JPEG", quality=88, optimize=True, progressive=True)
        print(f"    {branded_path.name:50s}  {w}x{h}  {branded_path.stat().st_size/1024:6.1f} KiB")


def main() -> int:
    p = argparse.ArgumentParser(description="GBP cover photo generator")
    p.add_argument("--source", default="../images/full/kitchen-dining-wide.jpg",
                   help="Source image path (default: kitchen-dining-wide.jpg)")
    p.add_argument("--config", default=str(ROOT / "logo_config.json"),
                   help="Logo config (for branding overlay colors / initials / fonts)")
    p.add_argument("--out", default=str(ROOT / "covers"),
                   help="Output directory (default: branding/covers/)")
    p.add_argument("--enhance", default="off", choices=["off", "moderate", "strong"],
                   help="Photographic enhancement (saturation/contrast/sharpness). off = pure crop.")
    p.add_argument("--h-bias", type=float, default=0.5,
                   help="Horizontal crop anchor: 0.0=left, 0.5=center (default), 1.0=right")
    p.add_argument("--v-bias", type=float, default=0.5,
                   help="Vertical crop anchor: 0.0=top, 0.5=center (default), 1.0=bottom")
    p.add_argument("--region", default=None,
                   help="Pre-crop region in source pixels: 'left,top,right,bottom'. "
                        "Use to drop unwanted edges (e.g., distracting signage) before 16:9 crop.")
    args = p.parse_args()

    region = None
    if args.region:
        try:
            region = tuple(int(x.strip()) for x in args.region.split(","))
            if len(region) != 4:
                raise ValueError("need 4 numbers")
        except Exception as exc:
            print(f"ERROR: --region must be 'left,top,right,bottom' integers. Got: {args.region}")
            return 1

    cfg_path = Path(args.config).resolve()
    if not cfg_path.exists():
        print(f"ERROR: config not found: {cfg_path}")
        return 1
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    source = (ROOT / args.source).resolve() if not Path(args.source).is_absolute() else Path(args.source)
    out_dir = Path(args.out).resolve()

    print(f"Site:   {cfg['site_name']}")
    print(f"Output: {out_dir}/")
    print()
    make_cover(source, out_dir, cfg, enhance=args.enhance, h_bias=args.h_bias,
               v_bias=args.v_bias, region=region)
    print()
    print("Done.")
    print(f"Recommended for GBP cover upload: cover_plain_*_1920.jpg or _2400.jpg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
