# SEO Ranking Tracker

Track how stationshotellet.com (or any future site) ranks on Google over time.

Append-only history → trend report. Reusable for next site builds.

## Quick start

```bash
cd c:/Git/Hotell/seo_tracker

# Day-0 baseline (free, automated, ~70s for 26 keywords)
python ranking_tracker.py check

# Generate visual report
python ranking_tracker.py report
# Open report.html in browser
```

## Three providers

| Provider | Cost | Accuracy | Speed | When to use |
|---|---|---|---|---|
| `duckduckgo` (default) | Free | Proxy for Google (~70-85% correlation) | ~70s for 26 kw | Weekly automated checks |
| `manual` | Free | Real Google data | ~5 min (you type) | When DDG starts blocking, or for definitive monthly check |
| `serper` | Free 2,500/mo, then $50/50k | Real Google data | ~30s for 26 kw | When ready for real automated tracking |

```bash
python ranking_tracker.py check --provider duckduckgo
python ranking_tracker.py check --provider manual
python ranking_tracker.py check --provider serper   # needs SERPER_API_KEY env var
```

For `serper`: sign up at https://serper.dev (free 2,500 queries/month), then:
```bash
$env:SERPER_API_KEY = "your-key-here"   # PowerShell
python ranking_tracker.py check --provider serper
```

## Manage the keyword list

```bash
python ranking_tracker.py list                       # show current keywords by tier
python ranking_tracker.py add "boende Norrbotten"    # add new keyword (interactive)
```

Or edit `config.json` directly.

## Files

- `config.json` — domain + keywords + tier config (edit this)
- `ranking_tracker.py` — main script
- `history.csv` — append-only log (commit this — it's the trend record)
- `report.html` — generated trend dashboard (regenerate on demand)

## Weekly automation (Telegram report every Sunday morning)

```bash
# One-shot manual trigger to test:
python ranking_tracker.py weekly --provider duckduckgo
# → runs check + regenerates report + posts week-over-week summary to Telegram

# Skip Telegram (still runs check + report):
python ranking_tracker.py weekly --no-telegram
```

**To install the scheduled task** (Sunday 03:00 PC-local time = ~09:00 Sweden):
```powershell
PowerShell -ExecutionPolicy Bypass -File install_schedule.ps1
```

This registers a Windows Scheduled Task `Stationshotellet_SEO_Weekly` that runs `run_weekly.bat` weekly. The bat file calls the Python tracker, which:
1. Runs `check` (logs rankings to `history.csv`)
2. Regenerates `report.html`
3. Sends a Telegram message comparing this week vs. last week

To uninstall: `Unregister-ScheduledTask -TaskName Stationshotellet_SEO_Weekly`

The Telegram message includes: total keywords found in top 50, new rankings this week, improvements, drops, and lost rankings. Empty weeks ("no movement") still send a brief status so you know it ran.

**Telegram config** is read from `c:/Git/ACSIL_Bots/gex/telegram_config.json` (existing setup). No additional config needed.

## Recommended cadence

- **Week 1:** Run daily via `duckduckgo` to confirm you're getting indexed
- **Week 2-4:** Auto-weekly via the scheduled task
- **Month 2+:** Sign up for `serper.dev` (free) and edit `run_weekly.bat` to use `--provider serper` for accurate Google data

## Reusing for next site

1. Edit `config.json` → change `domain`, `country_code`, `language`, `keywords`
2. Optionally rename `history.csv` to keep the prior site's data archived
3. Run `python ranking_tracker.py check`

The keyword tiering convention (T1=brand → T5=other-language) works for any site.

## Notes on what this can NOT tell you

- **Backlink count** — use Ahrefs/Semrush free tiers or `linkbuilder.io` for that
- **Why you're not ranking** — Google doesn't share that. Look at SERP and ask "what do top results have that I don't?"
- **Mobile vs desktop differences** — DDG/Serper return one ranking; Google can differ between devices
- **Personalized rankings** — incognito + manual is the only way to see what a stranger would see
