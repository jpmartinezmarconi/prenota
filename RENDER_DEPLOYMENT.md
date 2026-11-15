# 🚀 Guía de Deployment en Render

## ¿Qué es Render?

Render es una plataforma que permite ejecutar tu bot 24/7 en la nube de forma gratuita. Tu bot estará siempre verificando disponibilidad sin que necesites tener tu computadora prendida.

## Requisitos Previos

1. Account en GitHub (que ya tienes)
2. Account en Render (gratis)
3. Haber configurado y probado el bot localmente

## Paso 1: Preparar el Código

Todos los archivos necesarios ya están listos:

```
✓ bot.py           - Código del bot
✓ requirements.txt - Dependencias
✓ Dockerfile       - Configuración para Render
✓ .env.example     - Template de configuración
✓ .gitignore       - Protege tu .env (credenciales)
```

## Paso 2: Crear Account en Render

1. Ve a https://render.com
2. Click en "Sign up"
3. Conecta con GitHub
4. Autoriza el acceso

## Paso 3: Conectar tu Repositorio

1. En Render, ve a Dashboard
2. Click en "+ New"
3. Selecciona "Web Service"
4. Click en "Connect repository"
5. Busca "prenota"
6. Selecciona tu repo
7. Click en "Connect"

## Paso 4: Configurar el Servicio

Rellena los campos:

### Name
```
prenota-bot
```

### Environment
```
Python
```

### Build Command
```
pip install -r requirements.txt
```

### Start Command
```
python bot.py
```

### Plan
```
Free (recomendado para comenzar)
```

### Advanced Settings
- Deja los valores por defecto

## Paso 5: Configurar Variables de Entorno

1. Una vez creado el servicio, ve a la pestaña "Environment"
2. Click en "Add Environment Variable"
3. Añade cada una de estas variables (una por una):

### Variable 1: PRENOTAMI_EMAIL
- **Key**: `PRENOTAMI_EMAIL`
- **Value**: Tu email de Prenotami
- Click "Save"

### Variable 2: PRENOTAMI_PASSWORD
- **Key**: `PRENOTAMI_PASSWORD`
- **Value**: Tu contraseña de Prenotami
- Click "Save"

### Variable 3: TELEGRAM_TOKEN
- **Key**: `TELEGRAM_TOKEN`
- **Value**: Tu token de bot de Telegram (ejemplo: `123456789:ABCDEfghijklmnopqrstuvwxyz...`)
- Click "Save"

### Variable 4: CHAT_ID
- **Key**: `CHAT_ID`
- **Value**: Tu ID de chat de Telegram (es un número)
- Click "Save"

### Variable 5: BOOKING_URL
- **Key**: `BOOKING_URL`
- **Value**: La URL completa de tu cita en Prenotami
- **Ejemplo**: `https://prenotami.esteri.it/Services/Booking/12345`
- Click "Save"

### Variable 6: CHECK_INTERVAL_SECONDS (Opcional pero recomendado)
- **Key**: `CHECK_INTERVAL_SECONDS`
- **Value**: `300` (5 minutos - no lo hagas más bajo para no sobrecargar)
- Click "Save"

### Variable 7: SERVICE_NAME (Opcional)
- **Key**: `SERVICE_NAME`
- **Value**: `renovación de pasaporte`
- Click "Save"

## Paso 6: Iniciar el Servicio

1. En la página principal del servicio, verás un botón "Manual Deploy"
2. Click en "Deploy latest commit"
3. Render descargará tu código, instalará dependencias y iniciará el bot

## Paso 7: Verificar que Está Funcionando

1. Ve a la pestaña "Logs"
2. Deberías ver logs similares a:

```
2024-11-15 13:15:42 - INFO - ============================================================
2024-11-15 13:15:42 - INFO - 🚀 Iniciando bot de verificación de citas Prenota
2024-11-15 13:15:42 - INFO - ============================================================
2024-11-15 13:15:42 - INFO - ✅ Todas las variables de entorno están configuradas correctamente
2024-11-15 13:15:42 - INFO - Intervalo de verificación: 300 segundos
2024-11-15 13:15:42 - INFO - Servicio a monitorear: renovación de pasaporte

2024-11-15 13:15:43 - INFO - --- Iteración #1 ---
2024-11-15 13:15:43 - INFO - Iniciando sesión con email: tu-email@example.com
2024-11-15 13:15:45 - INFO - Login exitoso, verificando disponibilidad de citas...
2024-11-15 13:15:45 - INFO - ⏳ No hay citas disponibles. Próxima revisión en 300 segundos
```

✅ **¡Si ves esto, tu bot está funcionando correctamente!**

## Paso 8: Primera Prueba (Opcional)

Para verificar rápidamente que el bot puede enviar mensajes:

1. Ve a "Environment" en Render
2. Busca el servicio
3. Haz click en el botón de "Manual Deploy"
4. En logs deberías ver que envía un mensaje de prueba

O espera la próxima iteración (en 5 minutos si pusiste 300 segundos) para ver si funciona el login.

## 📊 Monitoreo Continuo

- El bot se ejecutará indefinidamente
- Cada `CHECK_INTERVAL_SECONDS` (por defecto 300 segundos = 5 minutos) verifica citas
- Cuando encuentre una, te enviará un mensaje por Telegram
- Los logs estarán disponibles en "Logs" en el dashboard

## Problemas Comunes

### ❌ "RuntimeError: Falta la variable de entorno X"

**Solución**: Verifica que todas las variables están en la pestaña "Environment"

### ❌ "Error 401"

**Solución**: Tus credenciales de Prenotami son incorrectas. Verifica email y contraseña en "Environment"

### ❌ "Error 403"

**Solución**: La BOOKING_URL es inválida o expiró. Conecta a Prenotami desde tu navegador, obtén una nueva URL y actualiza en "Environment"

### ❌ "RuntimeError: 401 Client Error"

**Solución**: Tu TELEGRAM_TOKEN o CHAT_ID son incorrectos. Verifica en "Environment"

### ✅ No veo logs

**Solución**: Los logs aparecen en tiempo real. Si el bot está corriendo sin errores, simplemente verás menos logs. Espera 5 minutos para ver la próxima iteración.

## Costos

- **Render Free Plan**: Incluye 750 horas/mes
- Tu bot usa ~24 horas/día = ~720 horas/mes
- **Total**: Cabe perfectamente en el plan gratuito ✅

## ¿Cómo detener el bot?

Si en algún momento necesitas pausar:

1. Ve al dashboard del servicio
2. Click en "Settings"
3. Desplázate al final
4. Click en "Suspend Service"

Para reanudarlo:
1. Click en "Resume Service"

## ¿Cómo ver si recibí citas disponibles?

El bot te enviará un mensaje de Telegram que se ve así:

```
✅ CITA DISPONIBLE

Hay cita disponible para renovación de pasaporte en Prenot@mi.
Revisa inmediatamente: https://prenotami.esteri.it/Services/Booking/...
```

---

**¡Listo! Tu bot está en la nube y funcionando 24/7** 🎉
