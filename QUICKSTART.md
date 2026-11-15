# ⚡ QuickStart - Prenota Bot en 5 minutos

## Para personas impacientes 😄

### Paso 1: Setup (3 minutos)

```bash
# Clonar
git clone https://github.com/jpmartinezmarconi/prenota.git
cd prenota

# Dependencias
pip install -r requirements.txt

# Configuración
cp .env.example .env
nano .env
# Rellena: PRENOTAMI_EMAIL, PRENOTAMI_PASSWORD, TELEGRAM_TOKEN, CHAT_ID, BOOKING_URL
```

### Paso 2: Probar Telegram (30 segundos)

```bash
python bot.py --test-telegram
```

Deberías recibir un mensaje en Telegram que diga: "Prueba correcta: el bot..."

### Paso 3: Probar búsqueda de citas (30 segundos)

```bash
python bot.py --once
```

Deberías ver logs mostrando que se conectó a Prenotami y verificó disponibilidad.

### Paso 4: Ejecutar en bucle (para desarrollo)

```bash
python bot.py
```

Se ejecutará cada 60 segundos (o lo que hayas configurado).

---

## ¿Cómo obtengo TELEGRAM_TOKEN y CHAT_ID?

### TELEGRAM_TOKEN:

1. Abre Telegram
2. Busca `@BotFather`
3. `/newbot`
4. Elige nombre y username
5. **Copia el token** (larga cadena con números y letras)

### CHAT_ID:

1. Envía cualquier mensaje a tu bot nuevo
2. En terminal, ejecuta:
   ```bash
   curl https://api.telegram.org/bot<TU_TOKEN>/getUpdates
   ```
   (Reemplaza `<TU_TOKEN>` con tu token)
3. Busca `"id":` en la respuesta
4. Ese número es tu CHAT_ID

---

## ¿Cómo obtengo BOOKING_URL?

1. Ve a https://prenotami.esteri.it
2. Inicia sesión
3. Navega hasta tu cita
4. **Copia la URL del navegador**
   - Ejemplo: `https://prenotami.esteri.it/Services/Booking/12345`
5. Pégala en `.env` como `BOOKING_URL`

---

## Solución Rápida de Problemas

| Problema | Solución |
|----------|----------|
| "Falta la variable..." | Edita `.env` y añade la variable que falta |
| "Error 401" | Credenciales Prenotami incorrectas |
| "Error 403" | BOOKING_URL inválida/expirada |
| No recibo mensaje en Telegram | Token o CHAT_ID incorrectos |
| Dice "No hay citas" | Normal, está funcionando 😊 |

---

## Deploy en Render (1 minuto)

```bash
# 1. Push a GitHub
git add -A
git commit -m "Configure bot"
git push origin main

# 2. Ve a https://render.com
# 3. Conecta tu repo
# 4. New Web Service
#    Environment: Python
#    Build: pip install -r requirements.txt
#    Start: python bot.py

# 5. Añade variables de entorno (igual que .env)

# 6. Deploy!
```

¡Tu bot corre 24/7 en Render! 🎉

---

## Comandos Útiles

```bash
# Verificar configuración
python verify_config.py

# Test rápido (una búsqueda)
python bot.py --once

# Test Telegram
python bot.py --test-telegram

# Con más logs
python -u bot.py

# Establecer intervalo (env var)
CHECK_INTERVAL_SECONDS=300 python bot.py
```

---

## ¿Funcionó? ✅

Si ves:
```
✅ Todas las variables de entorno están configuradas correctamente
--- Iteración #1 ---
Iniciando sesión con email: ...
Login exitoso, verificando disponibilidad de citas...
⏳ No hay citas disponibles
```

**¡PERFECTO!** Tu bot está funcionando. Ahora despliégalo en Render y olvídate.

---

**¿Preguntas?** Lee el [README.md](README.md) completo.

**¿Arquitectura?** Mira [ARCHITECTURE.md](ARCHITECTURE.md).

**¿Render?** Sigue [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md).
