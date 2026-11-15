#!/usr/bin/env python3
"""
Script para verificar la configuración de Prenota Bot
"""

import os
import sys
import logging
from pathlib import Path

# Añadir el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from bot import (
    required_setting,
    send_telegram_message,
    check_booking,
    LOGIN_URL,
    CHECK_INTERVAL_SECONDS,
    SERVICE_NAME,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def check_env_file():
    """Verificar que existe .env"""
    if not Path(".env").exists():
        logger.error("❌ Falta archivo .env")
        logger.info("   Ejecuta: cp .env.example .env")
        return False
    logger.info("✅ Archivo .env encontrado")
    return True


def check_required_variables():
    """Verificar todas las variables requeridas"""
    required_vars = [
        "PRENOTAMI_EMAIL",
        "PRENOTAMI_PASSWORD",
        "TELEGRAM_TOKEN",
        "CHAT_ID",
        "BOOKING_URL",
    ]
    
    all_ok = True
    for var in required_vars:
        try:
            value = required_setting(var)
            # Ocultar valores sensibles
            if "PASSWORD" in var or "TOKEN" in var:
                display_value = value[:4] + "*" * (len(value) - 4)
            else:
                display_value = value
            logger.info(f"✅ {var}: {display_value}")
        except RuntimeError as e:
            logger.error(f"❌ {var}: {e}")
            all_ok = False
    
    return all_ok


def test_telegram_connection():
    """Probar conexión a Telegram"""
    try:
        logger.info("🧪 Probando conexión a Telegram...")
        send_telegram_message("✅ Test exitoso: Bot de Prenota está configurado correctamente")
        logger.info("✅ Telegram funcionando correctamente")
        return True
    except Exception as e:
        logger.error(f"❌ Error al enviar mensaje a Telegram: {e}")
        return False


def test_booking_check():
    """Probar búsqueda de citas"""
    try:
        logger.info("🧪 Probando búsqueda de citas...")
        result = check_booking()
        if result:
            logger.warning("⚠️  Se encontró una cita disponible")
        else:
            logger.info("✅ Búsqueda funcionando (sin citas disponibles en este momento)")
        return True
    except Exception as e:
        logger.error(f"❌ Error al buscar citas: {type(e).__name__}: {e}")
        return False


def main():
    """Ejecutar verificaciones"""
    logger.info("=" * 60)
    logger.info("🔍 Verificando configuración de Prenota Bot")
    logger.info("=" * 60)
    
    checks = [
        ("Archivo .env", check_env_file),
        ("Variables de entorno", check_required_variables),
        ("Conexión a Telegram", test_telegram_connection),
        ("Búsqueda de citas", test_booking_check),
    ]
    
    results = {}
    for name, check_func in checks:
        logger.info(f"\n📋 {name}...")
        try:
            results[name] = check_func()
        except Exception as e:
            logger.error(f"❌ Error en verificación: {e}")
            results[name] = False
    
    # Resumen
    logger.info("\n" + "=" * 60)
    logger.info("📊 RESUMEN")
    logger.info("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅" if result else "❌"
        logger.info(f"{status} {name}")
    
    logger.info(f"\nResultado: {passed}/{total} verificaciones pasadas")
    
    if passed == total:
        logger.info("\n🎉 ¡Todo está configurado correctamente!")
        logger.info("\nPuedes iniciar el bot con:")
        logger.info("  python bot.py --once    (una verificación)")
        logger.info("  python bot.py            (monitoreo continuo)")
        return 0
    else:
        logger.error("\n❌ Hay problemas de configuración que necesitan ser corregidos")
        return 1


if __name__ == "__main__":
    sys.exit(main())
