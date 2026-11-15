# 🏗️ Arquitectura del Bot Prenota

## Flujo de Ejecución

```
┌─────────────────────────────────────────────────────────────┐
│                    BOT INICIADO                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         VALIDAR VARIABLES DE ENTORNO                        │
│   ✓ PRENOTAMI_EMAIL                                         │
│   ✓ PRENOTAMI_PASSWORD                                      │
│   ✓ TELEGRAM_TOKEN                                          │
│   ✓ CHAT_ID                                                 │
│   ✓ BOOKING_URL                                             │
└────────────────────┬────────────────────────────────────────┘
                     │
              ❌ Falta alguna
                     │
                     ▼
            ┌──────────────────┐
            │  EXIT CON ERROR  │
            └──────────────────┘
                     ▲
                     │
            ✅ Todas configuradas
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              LOOP PRINCIPAL (cada N segundos)               │
│                                                             │
│  1. AUTENTICARSE EN PRENOTAMI                               │
│     POST /Home/Login                                        │
│     ├─ Email: ${PRENOTAMI_EMAIL}                           │
│     └─ Password: ${PRENOTAMI_PASSWORD}                     │
│                                                             │
│  2. BUSCAR CITAS DISPONIBLES                                │
│     GET ${BOOKING_URL}                                      │
│     └─ ¿Contiene "${NO_APPOINTMENT_TEXT}"?                │
│                                                             │
│  3. SI HAY CITAS                                            │
│     POST api.telegram.org/bot${TOKEN}/sendMessage          │
│     ├─ chat_id: ${CHAT_ID}                                 │
│     └─ text: "✅ CITA DISPONIBLE..."                       │
│     └─ FINALIZAR                                           │
│                                                             │
│  4. SI NO HAY CITAS                                         │
│     └─ ESPERAR CHECK_INTERVAL_SECONDS (por defecto 60s)   │
│        └─ VOLVER AL PASO 1                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Componentes

### 1. **bot.py** 🤖
El corazón del sistema. Contiene:

```python
✓ required_setting()          → Obtiene variables de entorno
✓ send_telegram_message()     → Envía notificación a Telegram
✓ booking_available()         → Verifica si hay citas
✓ check_booking()             → Autentica y busca citas
✓ main()                      → Loop principal
```

### 2. **Configuración** ⚙️
Variables de entorno necesarias:

```
PRENOTAMI_EMAIL              Credenciales
PRENOTAMI_PASSWORD           para Prenotami

TELEGRAM_TOKEN               Credenciales
CHAT_ID                      para Telegram

BOOKING_URL                  URL específica de tu cita

CHECK_INTERVAL_SECONDS       Frecuencia (default: 60)
NO_APPOINTMENT_TEXT          Texto a detectar (default: "No hay...")
SERVICE_NAME                 Nombre del servicio (default: "renovación...")
```

### 3. **Integración Prenotami** 🏛️

```
https://prenotami.esteri.it/Home/Login
├─ POST con credenciales
├─ Establece sesión
└─ Permite acceder a BOOKING_URL
```

### 4. **Integración Telegram** 💬

```
https://api.telegram.org/bot{TOKEN}/sendMessage
├─ Chat ID destino
├─ Mensaje de notificación
└─ Confirmación de envío
```

## Modo Operación

### Modo Continuidad (Render)
```
┌──────────────┐
│  Render VM   │
├──────────────┤
│ bot.py       │  ← Ejecutándose 24/7
│ (siempre)    │
└──────────────┘
```

### Modo Desarrollo (Local)
```
┌──────────────────┐
│  Tu Computadora  │
├──────────────────┤
│ python bot.py    │  ← Mientras lo ejecutes
└──────────────────┘
```

### Modo Test
```
┌──────────────────────────────────┐
│  python bot.py --once            │
│  ✓ Una verificación              │
│  ✓ Exit después                  │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│  python bot.py --test-telegram   │
│  ✓ Envía mensaje de prueba       │
│  ✓ Exit después                  │
└──────────────────────────────────┘
```

## Flujo de Datos

```
┌─────────────────────────────────────────────────┐
│   USUARIO (tú)                                  │
│   Configura .env con credenciales              │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
        ┌──────────────────┐
        │   bot.py         │
        │ (en Render o     │
        │  localmente)     │
        └────┬─────────┬───┘
             │         │
      ┌──────▼──┐   ┌──▼──────┐
      │ Prenotami│   │ Telegram │
      │  (login) │   │  (notify)│
      └──────────┘   └──────────┘
             │              │
             └──────┬───────┘
                    │
                    ▼
        ┌──────────────────────┐
        │  TÚ recibes mensaje  │
        │  en Telegram cuando  │
        │  hay cita disponible │
        └──────────────────────┘
```

## Variables de Configuración

### Requeridas
| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `PRENOTAMI_EMAIL` | Email de tu cuenta Prenotami | juan@example.com |
| `PRENOTAMI_PASSWORD` | Contraseña Prenotami | MiPassword123! |
| `TELEGRAM_TOKEN` | Token del bot Telegram | 123456789:ABCDef... |
| `CHAT_ID` | Tu ID de chat Telegram | 987654321 |
| `BOOKING_URL` | URL de la cita en Prenotami | https://prenotami.esteri.it/Services/Booking/12345 |

### Opcionales
| Variable | Descripción | Valor por defecto |
|----------|-------------|------------------|
| `CHECK_INTERVAL_SECONDS` | Segundos entre verificaciones | 60 |
| `SERVICE_NAME` | Nombre del servicio monitoreado | renovación de pasaporte |
| `NO_APPOINTMENT_TEXT` | Texto a buscar cuando NO hay citas | No hay citas disponibles |

## Logs y Debugging

### Nivel INFO (por defecto)
```
2024-11-15 13:15:42 - INFO - Iniciando sesión con email: ...
2024-11-15 13:15:45 - INFO - Login exitoso, verificando...
2024-11-15 13:15:45 - INFO - ⏳ No hay citas disponibles
```

### Nivel DEBUG (si lo activas)
```
En bot.py, cambiar:
logging.basicConfig(level=logging.DEBUG)
```

Verás información adicional:
```
2024-11-15 13:15:45 - DEBUG - Respuesta de booking: 200, disponible: False
2024-11-15 13:15:45 - DEBUG - Contenido de la página (primeros 500 chars): ...
```

## Puntos Críticos para el Funcionamiento

```
┌─────────────────────────────────────────────────┐
│ 1. CREDENCIALES PRENOTAMI                       │
│    └─ Deben ser correctas y la cuenta activa    │
├─────────────────────────────────────────────────┤
│ 2. BOOKING_URL                                  │
│    └─ Debe ser válida y accesible               │
│    └─ Puede expirar (reiniciar sesión Prenotami)
├─────────────────────────────────────────────────┤
│ 3. TOKEN TELEGRAM                               │
│    └─ Debe ser válido y activo                  │
├─────────────────────────────────────────────────┤
│ 4. CHAT_ID TELEGRAM                             │
│    └─ Debe ser tu ID personal (no el del bot)   │
├─────────────────────────────────────────────────┤
│ 5. CONECTIVIDAD                                 │
│    └─ Acceso a https://prenotami.esteri.it      │
│    └─ Acceso a https://api.telegram.org         │
└─────────────────────────────────────────────────┘
```

## Ciclo de Vida de una Ejecución

```
START
  │
  ├─ Validar configuración
  │
  └─ LOOP:
      ├─ Conectar a Prenotami
      ├─ Autenticarse
      ├─ Acceder a BOOKING_URL
      ├─ Buscar NO_APPOINTMENT_TEXT
      │
      ├─ SI ENCUENTRA:
      │   └─ Enviar notificación Telegram
      │   └─ SALIR
      │
      ├─ SI NO ENCUENTRA:
      │   └─ Esperar CHECK_INTERVAL_SECONDS
      │   └─ Volver al inicio del LOOP
      │
      └─ SI ERROR:
          └─ Registrar error en logs
          └─ Esperar CHECK_INTERVAL_SECONDS
          └─ Reintentar
```

---

**El bot es simple pero efectivo: verifica, espera, repite.** 🔄
