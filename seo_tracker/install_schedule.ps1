# Install Windows Scheduled Task: Stationshotellet_SEO_Weekly
#
# Schedule: Sunday 03:00 PC-local time (= 09:00 Sweden time year-round, since
#   the PC is on US Eastern Time and Sweden is consistently ET+6 when both
#   sides are in the same DST phase, which they are most of the year).
#
# Action: runs c:\Git\Hotell\seo_tracker\run_weekly.bat which calls the
#   Python ranking tracker with the duckduckgo provider, regenerates report.html,
#   and posts the week-over-week summary to Telegram.
#
# To run: Right-click PowerShell -> Run as Administrator (only needed if your
# Windows policy requires it; otherwise current-user scheduled tasks are fine).
#
#     PowerShell -ExecutionPolicy Bypass -File install_schedule.ps1

$ErrorActionPreference = "Stop"

$TaskName = "Stationshotellet_SEO_Weekly"
$BatchPath = Join-Path $PSScriptRoot "run_weekly.bat"

if (-not (Test-Path $BatchPath)) {
    Write-Host "ERROR: $BatchPath not found." -ForegroundColor Red
    exit 1
}

# Remove existing task if present (idempotent)
$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Removing existing task $TaskName..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Build action: run the .bat file in its own directory
$Action = New-ScheduledTaskAction `
    -Execute "cmd.exe" `
    -Argument "/c `"$BatchPath`"" `
    -WorkingDirectory $PSScriptRoot

# Trigger: weekly on Sunday at 03:00 PC-local time (= 09:00 Sweden)
$Trigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek Sunday `
    -At 3am

# Settings: don't run while on battery? Actually let it run — small task.
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

# Principal: current interactive user (no special elevation needed)
$Principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "Weekly SEO ranking check for stationshotellet.com — sends Telegram summary every Sunday morning."

Write-Host ""
Write-Host "Installed: $TaskName" -ForegroundColor Green
Write-Host "Trigger:   Sunday 03:00 PC-local time (= ~09:00 Sweden time)"
Write-Host "Action:    $BatchPath"
Write-Host ""
Write-Host "Check it in Task Scheduler GUI: taskschd.msc -> Task Scheduler Library"
Write-Host "Or via PowerShell: Get-ScheduledTask -TaskName $TaskName"
Write-Host ""
Write-Host "Next scheduled run:"
(Get-ScheduledTask -TaskName $TaskName | Get-ScheduledTaskInfo).NextRunTime
