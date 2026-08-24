$ErrorActionPreference = "Stop"

function Set-SecretSetting($name, $prompt) {
    $secureValue = Read-Host -Prompt $prompt -AsSecureString
    $value = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureValue)
    )
    [Environment]::SetEnvironmentVariable($name, $value, "User")
}

Set-SecretSetting "PRENOTAMI_EMAIL" "Correo de Prenot@mi"
Set-SecretSetting "PRENOTAMI_PASSWORD" "Contraseña de Prenot@mi"
Set-SecretSetting "TELEGRAM_TOKEN" "Token nuevo de Telegram"
$chatId = Read-Host "Chat ID de Telegram"
$bookingUrl = Read-Host "URL real de Booking para renovación de pasaporte"
[Environment]::SetEnvironmentVariable("CHAT_ID", $chatId, "User")
[Environment]::SetEnvironmentVariable("BOOKING_URL", $bookingUrl, "User")
[Environment]::SetEnvironmentVariable("SERVICE_NAME", "renovación de pasaporte", "User")
[Environment]::SetEnvironmentVariable("CHECK_INTERVAL_SECONDS", "60", "User")
[Environment]::SetEnvironmentVariable("NO_APPOINTMENT_TEXT", "No hay citas disponibles", "User")

Write-Host "Configuración guardada para tu usuario."
& "$PSScriptRoot\install_task.ps1"
