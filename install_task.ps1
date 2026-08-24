$ErrorActionPreference = "Stop"

$project = $PSScriptRoot
$python = (Get-Command python).Source
$taskName = "Prenotami appointment checker"
$action = New-ScheduledTaskAction -Execute $python -Argument "`"$project\bot.py`"" -WorkingDirectory $project
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null
Write-Host "Tarea instalada: $taskName"
Write-Host "Se iniciará automáticamente al iniciar sesión en Windows."