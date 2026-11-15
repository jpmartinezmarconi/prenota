#!/bin/bash

# Script de setup para Prenota Bot

set -e

echo "🚀 Setup de Prenota Bot"
echo "======================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Verificar .env
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Falta archivo .env"
    echo "Copiaré .env.example a .env"
    cp .env.example .env
    echo ""
    echo "📝 Por favor, edita .env y completa:"
    echo "   - PRENOTAMI_EMAIL"
    echo "   - PRENOTAMI_PASSWORD"
    echo "   - TELEGRAM_TOKEN"
    echo "   - CHAT_ID"
    echo "   - BOOKING_URL"
    echo ""
    echo "Puedes editar el archivo con: nano .env"
else
    echo "✅ Archivo .env encontrado"
fi

echo ""
echo "✅ Setup completado"
echo ""
echo "Próximos pasos:"
echo "1. Configura tu .env si no lo has hecho"
echo "2. Prueba Telegram: python bot.py --test-telegram"
echo "3. Ejecuta una verificación: python bot.py --once"
echo "4. Inicia el monitoreo: python bot.py"
