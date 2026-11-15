# ✅ Checklist de Implementación - Prenota Bot

## Fase 1: Configuración Local (15 minutos)

### Preparación del Entorno
- [ ] Instalar Python 3.8+
- [ ] Clonar el repositorio
- [ ] Instalar dependencias: `pip install -r requirements.txt`

### Credenciales Prenotami
- [ ] Ir a https://prenotami.esteri.it
- [ ] Iniciar sesión con tu cuenta
- [ ] Navegar hasta tu cita de renovación de pasaporte
- [ ] Copiar la URL de la página (BOOKING_URL)
- [ ] Anotar email y contraseña

### Credenciales Telegram
- [ ] Abrir Telegram
- [ ] Buscar `@BotFather`
- [ ] Crear un nuevo bot con `/newbot`
- [ ] Copiar el token (TELEGRAM_TOKEN)
- [ ] Enviar un mensaje al bot
- [ ] Ejecutar `curl https://api.telegram.org/bot<TOKEN>/getUpdates`
- [ ] Obtener tu CHAT_ID de la respuesta

### Configurar .env
- [ ] Copiar `.env.example` a `.env`
- [ ] Rellenar PRENOTAMI_EMAIL
- [ ] Rellenar PRENOTAMI_PASSWORD
- [ ] Rellenar TELEGRAM_TOKEN
- [ ] Rellenar CHAT_ID
- [ ] Rellenar BOOKING_URL
- [ ] (Opcional) Rellenar CHECK_INTERVAL_SECONDS (recomendado: 300)

### Verificación Local
- [ ] Ejecutar `python verify_config.py`
- [ ] Todos los checks deben estar en VERDE ✅
- [ ] Ejecutar `python bot.py --test-telegram`
- [ ] Recibir mensaje de prueba en Telegram
- [ ] Ejecutar `python bot.py --once`
- [ ] Ver logs de conexión exitosa

---

## Fase 2: Testing Local (5 minutos)

### Test de Telegram
- [ ] Bot puede enviar mensajes
- [ ] CHAT_ID es correcto
- [ ] Mensajes llegan en tiempo real

### Test de Prenotami
- [ ] Login funciona (sin error 401)
- [ ] BOOKING_URL es accesible (sin error 403)
- [ ] Se detecta correctamente si hay citas

### Test de Bucle
- [ ] Ejecutar `python bot.py` por 5 minutos
- [ ] Verificar en logs que cada iteración funciona
- [ ] Ver que espera el intervalo configurado
- [ ] Presionar Ctrl+C para detener

---

## Fase 3: Deployment en Render (si deseas) - 10 minutos

### Preparar Repositorio
- [ ] Verificar que .env NO está en el repositorio
- [ ] Verificar que .gitignore incluye .env
- [ ] Hacer commit de todos los cambios
- [ ] Push a GitHub

### Crear Account en Render
- [ ] Ir a https://render.com
- [ ] Click "Sign Up"
- [ ] Conectar con GitHub
- [ ] Autorizar acceso al repositorio

### Crear Web Service
- [ ] Dashboard > + New > Web Service
- [ ] Seleccionar repositorio "prenota"
- [ ] Click "Connect"
- [ ] Rellenar:
  - Name: `prenota-bot`
  - Environment: `Python`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `python bot.py`
  - Plan: `Free` (gratuito)

### Configurar Variables de Entorno
- [ ] Ir a pestaña "Environment"
- [ ] Añadir PRENOTAMI_EMAIL
- [ ] Añadir PRENOTAMI_PASSWORD
- [ ] Añadir TELEGRAM_TOKEN
- [ ] Añadir CHAT_ID
- [ ] Añadir BOOKING_URL
- [ ] Añadir CHECK_INTERVAL_SECONDS (recomendado: 300)
- [ ] Guardar cambios

### Desplegar
- [ ] Click "Create Web Service"
- [ ] Esperar a que Render build y deploy
- [ ] Ir a pestaña "Logs"
- [ ] Verificar que el bot está ejecutándose
- [ ] Buscar el mensaje "Iteración #1"
- [ ] Verificar que no hay errores

### Verificación en Render
- [ ] El bot se ejecuta sin errores (ver logs)
- [ ] El bot se ejecuta cada N segundos (ver logs)
- [ ] Puedes pausar/reanudar el servicio

---

## Fase 4: Operación Continua

### Monitoreo Regular
- [ ] Revisar logs en Render cada 1-2 días
- [ ] Verificar que el bot no tiene errores persistentes
- [ ] Comprobar que recibiste notificación si hubiera citas

### Mantenimiento
- [ ] Si BOOKING_URL deja de funcionar:
  - [ ] Conectar a Prenotami desde navegador
  - [ ] Obtener nueva URL
  - [ ] Actualizar en Render (Environment)
- [ ] Si cambias contraseña de Prenotami:
  - [ ] Actualizar PRENOTAMI_PASSWORD en Render
- [ ] Si cambias contraseña de Telegram:
  - [ ] Actualizar TELEGRAM_TOKEN en Render

### Troubleshooting
- [ ] Ver sección "Solución de Problemas" en README.md
- [ ] Ejecutar `python verify_config.py` si algo falla
- [ ] Revisar logs en Render (pestaña "Logs")
- [ ] Probar localmente: `python bot.py --once`

---

## Fase 5: Cuando Encuentres Cita

### Señal de Éxito
- [ ] Recibes mensaje en Telegram diciendo:
  ```
  ✅ CITA DISPONIBLE
  Hay cita disponible para renovación de pasaporte...
  ```

### Acciones Inmediatas
- [ ] Abrir el link de la notificación
- [ ] Reservar la cita en Prenotami
- [ ] (Opcional) Pausar el bot en Render si ya no lo necesitas
- [ ] Celebrar 🎉

---

## Documentación de Referencia

Si necesitas ayuda:

| Pregunta | Documento |
|----------|-----------|
| "¿Cómo empiezo?" | [QUICKSTART.md](QUICKSTART.md) |
| "¿Cómo configuro?" | [README.md](README.md) |
| "¿Cómo despliego?" | [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) |
| "¿Cómo funciona?" | [ARCHITECTURE.md](ARCHITECTURE.md) |
| "¿Qué está mal?" | [README.md - Troubleshooting](README.md#solución-de-problemas) |

---

## Comandos de Referencia Rápida

```bash
# Verificar configuración
python verify_config.py

# Test de Telegram
python bot.py --test-telegram

# Una búsqueda
python bot.py --once

# Ejecución continua local
python bot.py

# Ver logs detallados
python -u bot.py

# Con intervalo personalizado
CHECK_INTERVAL_SECONDS=300 python bot.py
```

---

## Notas Importantes

⚠️ **Seguridad**
- Nunca hagas commit de `.env` con credenciales
- El `.gitignore` lo protege automáticamente
- En Render, las variables se guardan encriptadas

⚠️ **Prenotami**
- BOOKING_URL puede expirar
- Si deja de funcionar, obtén una nueva
- La contraseña se envía en cada login (segura)

⚠️ **Telegram**
- El token permite enviar mensajes como tu bot
- El CHAT_ID debe ser tu ID personal
- No compartas el token

⚠️ **Render**
- Gratis hasta 750 horas/mes
- Tu bot usa ~720 horas/mes (24/7)
- Cabe en el plan gratuito

---

## Estado Final

Cuando hayas completado TODO:

```
✅ Bot configurado localmente
✅ Telegram funciona
✅ Búsqueda de citas funciona
✅ Bot desplegado en Render (opcional)
✅ Listo para encontrar tu cita 🎉
```

---

**¡Felicidades! Tu bot de Prenotami está listo.** 🚀

Ahora solo espera a que te avise cuando haya cita disponible.

