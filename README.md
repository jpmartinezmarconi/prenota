# Prenota Bot 🤖

Bot automático para verificar disponibilidad de citas en Prenotami (Consulado Italiano en Barcelona) y notificarte por Telegram.

## 📋 Requisitos

- Python 3.8+
- Cuenta en [Prenotami](https://prenotami.esteri.it)
- Bot de Telegram con acceso a tu chat

## 🚀 Setup Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/jpmartinezmarconi/prenota.git
cd prenota
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copiar `.env.example` a `.env` y completar con tus datos:

```bash
cp .env.example .env
```

**Variables requeridas:**

- `PRENOTAMI_EMAIL`: Tu email de Prenotami
- `PRENOTAMI_PASSWORD`: Tu contraseña de Prenotami
- `BOOKING_URL`: URL de tu cita (obténla de la interfaz web)
- `TELEGRAM_TOKEN`: Token del bot de Telegram
- `CHAT_ID`: Tu ID de chat de Telegram (donde recibirás notificaciones)

**Variables opcionales:**

- `CHECK_INTERVAL_SECONDS`: Intervalo entre verificaciones (default: 60)
- `SERVICE_NAME`: Nombre del servicio a monitorear (default: "renovación de pasaporte")
- `NO_APPOINTMENT_TEXT`: Texto que indica "no hay citas" (default: "No hay citas disponibles")

### 4. Obtener credenciales de Telegram

1. Busca `@BotFather` en Telegram
2. Crea un nuevo bot con `/newbot`
3. Copia el token (formato: `123456789:ABCDEfghijklmnopqrstuvwxyz...`)
4. Envía cualquier mensaje a tu bot
5. Ejecuta: `curl https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
6. Busca tu `chat_id` en la respuesta (generalmente un número negativo o positivo)

### 5. Obtener BOOKING_URL

1. Inicia sesión en https://prenotami.esteri.it
2. Navega hasta tu cita
3. Copia la URL actual de tu navegador
4. Ejemplo: `https://prenotami.esteri.it/Services/Booking/123456`

## 🧪 Pruebas

### Probar conexión a Telegram

```bash
python bot.py --test-telegram
```

Deberías recibir un mensaje en tu chat de Telegram.

### Ejecutar una única verificación

```bash
python bot.py --once
```

Verifica disponibilidad una sola vez y muestra logs detallados.

### Ejecutar en bucle continuo

```bash
python bot.py
```

Se ejecutará indefinidamente, revisando cada `CHECK_INTERVAL_SECONDS`.

## 🐳 Deployment en Render

### 1. Crear archivo `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

CMD ["python", "bot.py"]
```

### 2. Crear archivo `render.yaml` (opcional, para CI/CD)

```yaml
services:
  - type: web
    name: prenota-bot
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python bot.py
    envVars:
      - key: PRENOTAMI_EMAIL
        sync: false
      - key: PRENOTAMI_PASSWORD
        sync: false
      - key: TELEGRAM_TOKEN
        sync: false
      - key: CHAT_ID
        sync: false
      - key: BOOKING_URL
        sync: false
```

### 3. Pasos en Render

1. Conecta tu repositorio a [Render.com](https://render.com)
2. Crea un nuevo servicio "Web Service"
3. Selecciona tu repositorio
4. Configura:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
5. Ve a "Environment" y añade tus variables:
   - `PRENOTAMI_EMAIL`
   - `PRENOTAMI_PASSWORD`
   - `TELEGRAM_TOKEN`
   - `CHAT_ID`
   - `BOOKING_URL`
   - `CHECK_INTERVAL_SECONDS` (recomendado: 300 o más para no sobrecargar)

## 🔍 Solución de problemas

### "Falta la variable de entorno X"

Verifica que todas las variables requeridas están en tu archivo `.env` o en las variables de entorno del sistema.

### "Error durante la revisión: 401"

Probablemente tus credenciales de Prenotami son incorrectas. Verifica email y contraseña.

### "Error durante la revisión: 403"

La URL de booking puede ser inválida o haber expirado. Inicia sesión nuevamente en Prenotami y obtén una nueva URL.

### "No funciona en Render"

1. Revisa los logs en Render: Dashboard > Bot > Logs
2. Verifica que todas las variables de entorno están configuradas
3. Prueba localmente con `python bot.py --once`

## 📊 Monitoreo

Para ver qué está haciendo el bot:

```bash
# Ver logs en tiempo real (si ejecutas en la terminal)
python bot.py

# Ver solo un chequeo
python bot.py --once
```

## 🛡️ Seguridad

⚠️ **NUNCA** hagas commit de tu `.env` con credenciales reales. El `.gitignore` ya tiene esta regla.

## 📝 Licencia

MIT

## ¿Preguntas?

Abre un issue en el repositorio.
