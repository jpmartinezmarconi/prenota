import logging
import os
import sys
import time

import requests
from dotenv import load_dotenv

load_dotenv()


LOGIN_URL = "https://prenotami.esteri.it/Home/Login"
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))
NO_APPOINTMENT_TEXT = os.getenv("NO_APPOINTMENT_TEXT", "No hay citas disponibles")
SERVICE_NAME = os.getenv("SERVICE_NAME", "renovación de pasaporte")

HEADERS = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Language": "es-ES,es;q=0.9",
	"Accept-Encoding": "gzip, deflate",
	"DNT": "1",
	"Connection": "keep-alive",
	"Upgrade-Insecure-Requests": "1",
}


def required_setting(name):
	value = os.getenv(name)
	if not value:
		raise RuntimeError(f"Falta la variable de entorno {name}")
	return value


def send_telegram_message(message):
	token = required_setting("TELEGRAM_TOKEN")
	chat_id = required_setting("CHAT_ID")
	response = requests.post(
		f"https://api.telegram.org/bot{token}/sendMessage",
		data={"chat_id": chat_id, "text": message},
		timeout=20,
	)
	response.raise_for_status()


def booking_available(session, booking_url):
	response = session.get(booking_url, timeout=30)
	response.raise_for_status()
	
	# Verificar si hay citas disponibles
	# Busca el texto que CONFIRMA que NO hay citas
	no_appointment_found = NO_APPOINTMENT_TEXT.lower() in response.text.lower()
	available = not no_appointment_found
	
	logging.info(f"Respuesta de booking: {response.status_code}")
	logging.info(f"¿'No hay citas disponibles' encontrado en página?: {no_appointment_found}")
	logging.info(f"¿Citas disponibles?: {available}")
	logging.debug(f"Contenido de la página (primeros 500 chars): {response.text[:500]}")
	
	return available


def check_booking():
	email = required_setting("PRENOTAMI_EMAIL")
	password = required_setting("PRENOTAMI_PASSWORD")
	booking_url = required_setting("BOOKING_URL")

	with requests.Session() as session:
		session.headers.update(HEADERS)
		logging.info(f"Iniciando sesión con email: {email}")
		response = session.post(
			LOGIN_URL,
			data={"Email": email, "Password": password},
			timeout=30,
		)
		response.raise_for_status()
		
		# Verificar que el login fue exitoso
		if "error" in response.text.lower() or response.status_code != 200:
			logging.warning(f"Posible error en login: {response.status_code}")
		
		logging.info("Login exitoso, verificando disponibilidad de citas...")
		if booking_available(session, booking_url):
			message = f"✅ CITA DISPONIBLE\n\nHay cita disponible para {SERVICE_NAME} en Prenot@mi.\nRevisa inmediatamente: {booking_url}"
			send_telegram_message(message)
			logging.warning("⚠️ NOTIFICACIÓN DE CITA ENVIADA POR TELEGRAM")
			return True
		else:
			logging.info("✅ Verificación completada: No hay citas disponibles en este momento")
	return False


def main(run_once=False):
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(levelname)s - %(message)s",
	)
	
	logging.info("=" * 60)
	logging.info("🚀 Iniciando bot de verificación de citas Prenota")
	logging.info("=" * 60)
	
	# Validar que todas las variables requeridas estén configuradas
	try:
		required_setting("PRENOTAMI_EMAIL")
		required_setting("PRENOTAMI_PASSWORD")
		required_setting("TELEGRAM_TOKEN")
		required_setting("CHAT_ID")
		required_setting("BOOKING_URL")
		logging.info("✅ Todas las variables de entorno están configuradas correctamente")
	except RuntimeError as e:
		logging.error(f"❌ Error de configuración: {e}")
		sys.exit(1)

	logging.info(f"Intervalo de verificación: {CHECK_INTERVAL_SECONDS} segundos")
	logging.info(f"Servicio a monitorear: {SERVICE_NAME}")
	
	iteration = 0
	cita_enviada = False
	while True:
		iteration += 1
		try:
			logging.info(f"\n--- Iteración #{iteration} ---")
			if check_booking():
				if not cita_enviada:
					logging.info("✅ Cita encontrada y notificación enviada.")
					cita_enviada = True
				logging.info(f"⏳ Continuando monitoreo. Próxima revisión en {CHECK_INTERVAL_SECONDS} segundos")
			else:
				cita_enviada = False
				logging.info(f"⏳ No hay citas disponibles. Próxima revisión en {CHECK_INTERVAL_SECONDS} segundos")
		except Exception as e:
			logging.exception(f"❌ Error durante la revisión: {type(e).__name__}: {e}")
		
		if run_once:
			logging.info("Modo de ejecución única activado. Finalizando.")
			return
		
		time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
	if "--test-telegram" in sys.argv:
		send_telegram_message("Prueba correcta: el bot de Prenot@mi puede enviarte mensajes.")
	else:
		main(run_once="--once" in sys.argv)
