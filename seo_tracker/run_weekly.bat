@echo off
REM Weekly SEO ranking check — invoked by Windows Scheduled Task.
REM Uses Serper.dev (real Google data); reads API key from serper_config.json.
cd /d "%~dp0"
python ranking_tracker.py weekly --provider serper >> weekly_run.log 2>&1
