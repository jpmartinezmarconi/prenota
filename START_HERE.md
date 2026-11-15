# 🚀 START HERE - Prenota Bot

## ¿Qué es esto?

Un bot que automaticamente te notifica por Telegram cuando hay citas disponibles para renovar tu pasaporte en el consulado italiano en Barcelona (Prenotami).

## ¿Qué encontrarás?

### 📚 Documentación (Lee en este orden)

1. **[QUICKSTART.md](QUICKSTART.md)** ⚡
   - 5 minutos para empezar
   - Comandos rápidos
   - Solución de problemas inmediata
   - **EMPIEZA AQUÍ**

2. **[README.md](README.md)** 📖
   - Guía completa de setup
   - Cómo obtener credenciales de Telegram
   - Cómo obtener BOOKING_URL
   - Troubleshooting detallado

3. **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** 🚀
   - Deploy en la nube (24/7)
   - Paso a paso con instrucciones visuales
   - Asegura que tu bot corre siempre

4. **[ARCHITECTURE.md](ARCHITECTURE.md)** 📐
   - Diagramas de flujo
   - Cómo funciona internamente
   - Componentes y conexiones

5. **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)** ✅
   - Checklist de 5 fases
   - Desde setup hasta Render
   - Referencia rápida de comandos

---

## 🎯 Setup Rápido (5 minutos)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Crear configuración
cp .env.example .env
nano .env  # Rellenar con tus datos

# 3. Verificar configuración
python verify_config.py

# 4. Probar Telegram
python bot.py --test-telegram

# 5. Probar búsqueda de citas
python bot.py --once
```

---

## 📋 Qué Necesitas

### Credenciales Prenotami
- Email
- Contraseña
- URL de tu cita (BOOKING_URL)

### Credenciales Telegram
- Token del bot (de @BotFather)
- Tu CHAT_ID

---

## ✨ Lo que el bot hace

```
Cada X segundos (por defecto 60):
  1. Conectarse a Prenotami
  2. Verificar si hay citas disponibles
  3. Si las hay:
     - Enviarte un mensaje por Telegram
     - Terminar la ejecución
  4. Si no:
     - Esperar X segundos
     - Repetir
```

---

## 🚀 Opciones de Ejecución

### Local (mientras tu PC está prendida)
```bash
python bot.py
```

### Una verificación
```bash
python bot.py --once
```

### Test de Telegram
```bash
python bot.py --test-telegram
```

### En la nube (24/7 - RECOMENDADO)
1. Seguir [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
2. Tu bot correrá automáticamente

---

## 🔍 ¿Cómo Verifico que Funciona?

```bash
# Esto debería dar VERDE en todo
python verify_config.py

# Si todo está verde, tu bot está listo
```

---

## ⚠️ Puntos Importantes

1. **BOOKING_URL puede expirar**
   - Si deja de funcionar, obtén una nueva en Prenotami

2. **No hagas commit de .env**
   - El .gitignore lo protege automáticamente
   - Nunca publiques credenciales

3. **En Render usa intervalos largos**
   - CHECK_INTERVAL_SECONDS = 300 (5 minutos mínimo)

4. **Las credenciales son sensibles**
   - No las compartas
   - Telegram token = acceso para enviar mensajes

---

## 📖 Documentación por Caso de Uso

| Necesito... | Leo... |
|-------------|--------|
| Empezar ahora | QUICKSTART.md |
| Configurar todo | README.md |
| Desplegar en Render | RENDER_DEPLOYMENT.md |
| Entender el código | ARCHITECTURE.md |
| Seguir un checklist | IMPLEMENTATION_CHECKLIST.md |
| Solucionar problemas | README.md (Troubleshooting) |

---

## 🎉 Cuando Encuentres Cita

Recibirás un mensaje en Telegram:
```
✅ CITA DISPONIBLE

Hay cita disponible para renovación de pasaporte en Prenot@mi.
Revisa inmediatamente: https://prenotami.esteri.it/...
```

Haz click en el link y reserva tu cita.

---

## 🆘 Algo No Funciona

1. Ejecuta `python verify_config.py`
2. Busca tu problema en README.md (Troubleshooting)
3. Lee ARCHITECTURE.md para entender el flujo

---

## 📁 Archivos Principales

```
.
├── bot.py                      # Código principal
├── verify_config.py            # Valida configuración
├── requirements.txt            # Dependencias
├── Dockerfile                  # Para Render
├── .env.example                # Template
├── setup.sh                    # Setup automático
│
├── START_HERE.md              # Este archivo
├── QUICKSTART.md              # 5 minutos ⚡
├── README.md                  # Guía completa 📖
├── RENDER_DEPLOYMENT.md       # Deploy 🚀
├── ARCHITECTURE.md            # Cómo funciona 📐
└── IMPLEMENTATION_CHECKLIST.md # Fases ✅
```

---

## ✅ Checklist Rápido

- [ ] Leí QUICKSTART.md
- [ ] Configuré .env
- [ ] Ejecuté `python verify_config.py`
- [ ] Ejecuté `python bot.py --test-telegram`
- [ ] Ejecuté `python bot.py --once`
- [ ] (Opcional) Desplegué en Render

---

## 🎓 Recursos

- [Prenotami](https://prenotami.esteri.it) - Web del servicio
- [Telegram Bot API](https://core.telegram.org/bots) - Documentación de bots
- [Render.com](https://render.com) - Plataforma de deploy

---

**¡Bienvenido! Empieza por [QUICKSTART.md](QUICKSTART.md)** ⚡

El bot te avisará cuando encuentre cita disponible. ¡Buena suerte! 🍀
