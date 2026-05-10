# Logo generator (config-driven, reusable)

Generates polished circle-badge logos from a JSON config. Reuse for any future
site by editing the config — no code changes needed.

## What it produces

Two output families per run:

**Full badge** (initials + wordmark + subtitle, in a double-ring) — recommended
for Google Business Profile, social media headers, "About Us" pages.
- `logo_full_720.png` — primary GBP profile photo upload
- `logo_full_512.png` — Instagram, Facebook, LinkedIn header avatars
- `logo_full_256.png` — small thumbnails

**Mark-only** (just initials in the ring) — recommended for tight spaces where
the wordmark would be illegible.
- `logo_mark_720.png` — large icon
- `logo_mark_256.png` — site favicon source
- `logo_mark_128.png` — bookmark icon
- `logo_mark_64.png`  — tiny tab icon

## Quick start

```bash
cd c:/Git/Hotell/branding
python logo_generator.py
# → reads logo_config.json, writes 7 PNGs to logos/
```

## Reuse for a new site

1. Copy the existing config:
   ```bash
   cp logo_config.json logo_config_mybook.json
   ```
2. Edit the new file:
   ```json
   {
     "site_name": "My New Site",
     "initials": "MN",
     "wordmark": "My New Site",
     "subtitle": "C I T Y   ·   C O U N T R Y",
     "colors": {
       "background": "#fff8f0",
       "accent":     "#1f3a5f",
       "text":       "#101820"
     },
     ...
   }
   ```
3. Run with the new config:
   ```bash
   python logo_generator.py --config logo_config_mybook.json
   ```

The output folder name comes from `output_dir` in the config — set it to a
site-specific path (e.g., `"logos_mybook"`) so each site's logos stay separate.

## Config field reference

| Field | What it is | Example |
|---|---|---|
| `site_name` | Bookkeeping label, printed to console | `"Stations Hotellet"` |
| `initials` | Big monogram in the center | `"SH"` (1-3 chars works best) |
| `wordmark` | Larger text below the divider | `"Stations Hotellet"` |
| `subtitle` | Small text below the wordmark | `"Ö J E B Y N   ·   S V E R I G E"` |
| `colors.background` | Canvas color | `"#faf7f2"` cream |
| `colors.accent` | Ring + initials + subtitle | `"#7d5e08"` deep gold |
| `colors.text` | Wordmark | `"#1a150d"` near-black |
| `fonts.monogram` | Font for initials (Windows fonts dir) | `"georgiab.ttf"` |
| `fonts.wordmark` | Font for site name | `"georgiab.ttf"` |
| `fonts.subtitle` | Font for tagline | `"georgia.ttf"` |
| `output_dir` | Subfolder for PNGs | `"logos"` |
| `output_sizes.full` | List of full-badge sizes | `[720, 512, 256]` |
| `output_sizes.mark` | List of mark-only sizes | `[720, 256, 128, 64]` |

## Font choices

Default uses **Georgia / Georgia Bold** — classic serif, on every Windows
machine, reads as "established / boutique / hotel."

For a different vibe try:
- `"arial.ttf"` / `"arialbd.ttf"` — modern sans-serif (tech, clean)
- `"calibri.ttf"` / `"calibrib.ttf"` — friendly sans-serif (consumer, warm)
- `"times.ttf"` / `"timesbd.ttf"` — traditional serif (formal, heritage)

Files are looked up in `C:/Windows/Fonts/`. Run `dir /b C:\Windows\Fonts\*.ttf`
to see what's available.

## Color palette tips

For best contrast and a polished look:
- `background` should be light (cream, off-white, pale grey)
- `accent` should pass WCAG AA on the background — at least 4.5:1 contrast.
  Use https://webaim.org/resources/contrastchecker/ to verify.
- `text` should be near-black for the wordmark — high contrast, easy to read.

The Stationshotellet defaults (cream / deep gold #7d5e08 / near-black) all
pass WCAG AA — same palette as the live site.

## Why two variants?

- **Full badge** has a rich brand presence — read at medium-large sizes.
- **Mark-only** stays legible at 16×16 favicon size where the wordmark would
  be indistinguishable mush.

Use both. Most sites use the full badge for headers and social profiles,
mark-only for favicon and small UI chrome.
