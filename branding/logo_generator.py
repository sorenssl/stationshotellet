"""Config-driven logo generator. Reusable across sites — edit logo_config.json
(or pass --config path/to/other.json) to brand a new site without code changes.

Two output families per run:
  full/  — circle badge with initials + wordmark + subtitle
           (recommended for Google Business Profile, social media headers)
  mark/  — minimalist initials inside double-ring only
           (recommended for favicon and tiny thumbnails)

Colors, fonts, initials, wordmark, subtitle all live in the config file.

Run:
    python logo_generator.py                              # uses logo_config.json
    python logo_generator.py --config other_site.json     # different config
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent


def _hex_to_rgb(value) -> tuple[int, int, int]:
    """Accept '#RRGGBB' or [r, g, b]. Returns (r, g, b)."""
    if isinstance(value, (list, tuple)) and len(value) == 3:
        return tuple(int(c) for c in value)
    s = str(value).lstrip("#")
    if len(s) != 6:
        raise ValueError(f"Bad color: {value}")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def _font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for candidate in [name, "georgia.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _centered_x(draw: ImageDraw.ImageDraw, text: str,
                font: ImageFont.FreeTypeFont, canvas_size: int) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    return (canvas_size - w) // 2 - bbox[0]


def _draw_double_ring(draw: ImageDraw.ImageDraw, size: int, accent: tuple) -> None:
    margin_outer = int(size * 0.05)
    margin_inner = int(size * 0.08)
    ring_thick = max(2, int(size * 0.012))
    ring_thin = max(1, int(size * 0.004))
    draw.ellipse(
        [(margin_outer, margin_outer), (size - margin_outer, size - margin_outer)],
        outline=accent, width=ring_thick,
    )
    draw.ellipse(
        [(margin_inner, margin_inner), (size - margin_inner, size - margin_inner)],
        outline=accent, width=ring_thin,
    )


def make_mark(size: int, out_path: Path, cfg: dict) -> None:
    """Mark-only variant — just the initials in a double ring. Scales to favicon."""
    bg = _hex_to_rgb(cfg["colors"]["background"])
    accent = _hex_to_rgb(cfg["colors"]["accent"])

    img = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(img)
    _draw_double_ring(draw, size, accent)

    # Initials, large and confident, with slight upward optical centering
    mono_font = _font(cfg["fonts"]["monogram"], int(size * 0.42))
    text = cfg["initials"]
    bbox = draw.textbbox((0, 0), text, font=mono_font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (size - w) // 2 - bbox[0]
    y = (size - h) // 2 - bbox[1] - int(size * 0.02)
    draw.text((x, y), text, font=mono_font, fill=accent)

    img.save(out_path, "PNG", quality=95, optimize=True)


def make_full(size: int, out_path: Path, cfg: dict) -> None:
    """Full badge — initials + divider + wordmark + subtitle. Tighter ring fit."""
    bg = _hex_to_rgb(cfg["colors"]["background"])
    accent = _hex_to_rgb(cfg["colors"]["accent"])
    text_color = _hex_to_rgb(cfg["colors"]["text"])

    img = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(img)
    _draw_double_ring(draw, size, accent)

    # Initials — sized so wordmark + subtitle have room below
    mono_font = _font(cfg["fonts"]["monogram"], int(size * 0.26))
    initials = cfg["initials"]
    bbox = draw.textbbox((0, 0), initials, font=mono_font)
    mono_w = bbox[2] - bbox[0]
    mono_h = bbox[3] - bbox[1]
    mono_x = (size - mono_w) // 2 - bbox[0]
    mono_y = int(size * 0.20) - bbox[1]
    draw.text((mono_x, mono_y), initials, font=mono_font, fill=accent)

    # Decorative divider — thin gold line with end-cap dots
    div_y = mono_y + mono_h + int(size * 0.05)
    div_half = int(size * 0.085)
    cx = size // 2
    line_w = max(1, int(size * 0.0055))
    draw.line(
        [(cx - div_half, div_y), (cx + div_half, div_y)],
        fill=accent, width=line_w,
    )
    cap_r = max(2, int(size * 0.009))
    for x in (cx - div_half, cx + div_half):
        draw.ellipse(
            [(x - cap_r, div_y - cap_r), (x + cap_r, div_y + cap_r)],
            fill=accent,
        )

    # Wordmark
    wm_font = _font(cfg["fonts"]["wordmark"], int(size * 0.075))
    wm_text = cfg["wordmark"]
    wm_x = _centered_x(draw, wm_text, wm_font, size)
    wm_y = div_y + int(size * 0.045)
    draw.text((wm_x, wm_y), wm_text, font=wm_font, fill=text_color)

    # Subtitle
    sub_font = _font(cfg["fonts"]["subtitle"], int(size * 0.038))
    sub_text = cfg["subtitle"]
    sub_x = _centered_x(draw, sub_text, sub_font, size)
    sub_y = wm_y + int(size * 0.10)
    draw.text((sub_x, sub_y), sub_text, font=sub_font, fill=accent)

    img.save(out_path, "PNG", quality=95, optimize=True)


def main() -> int:
    p = argparse.ArgumentParser(description="Logo generator (config-driven)")
    p.add_argument("--config", default=str(ROOT / "logo_config.json"),
                   help="Path to logo config JSON (default: logo_config.json next to this script)")
    args = p.parse_args()

    cfg_path = Path(args.config).resolve()
    if not cfg_path.exists():
        print(f"ERROR: config not found: {cfg_path}")
        return 1
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    out_dir = (cfg_path.parent / cfg.get("output_dir", "logos")).resolve()
    out_dir.mkdir(exist_ok=True)

    print(f"Site: {cfg['site_name']}")
    print(f"Config: {cfg_path}")
    print(f"Output: {out_dir}/")
    print()

    print("Full badge (initials + wordmark + subtitle):")
    for sz in cfg["output_sizes"]["full"]:
        path = out_dir / f"logo_full_{sz}.png"
        make_full(sz, path, cfg)
        print(f"  {path.name:24s}  {sz}x{sz}  {path.stat().st_size/1024:5.1f} KiB")
    print()

    print("Mark-only (initials in ring):")
    for sz in cfg["output_sizes"]["mark"]:
        path = out_dir / f"logo_mark_{sz}.png"
        make_mark(sz, path, cfg)
        print(f"  {path.name:24s}  {sz}x{sz}  {path.stat().st_size/1024:5.1f} KiB")
    print()
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
