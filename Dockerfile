FROM python:3.11-slim

WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY bot.py .

# Ejecutar el bot
CMD ["python", "bot.py"]
