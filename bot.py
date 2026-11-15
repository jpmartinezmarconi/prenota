import logging
import os
import sys
import time

import requests
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def check_booking():
	email = required_setting("PRENOTAMI_EMAIL")
	password = required_setting("PRENOTAMI_PASSWORD")
	booking_url = required_setting("BOOKING_URL")

	try:
		logging.info("Iniciando navegador anti-detección...")
		
		# Usar undetected-chromedriver para evitar CAPTCHA
		driver = uc.Chrome(headless=True, use_subprocess=False)
		
		try:
			logging.info(f"Navegando a login...")
			driver.get("https://prenotami.esteri.it/Home/Login")
			
			# Esperar a que se cargue el formulario de login
			wait = WebDriverWait(driver, 15)
			email_field = wait.until(EC.presence_of_element_located((By.NAME, "Email")))
			
			logging.info(f"Iniciando sesión con email: {email}")
			email_field.send_keys(email)
			
			password_field = driver.find_element(By.NAME, "Password")
			password_field.send_keys(password)
			
			# Buscar y hacer click en el botón de login
			login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
			login_button.click()
			
			# Esperar a que se cargue la página después del login
			time.sleep(3)
			
			logging.info("Login completado, navegando a citas...")
			driver.get(booking_url)
			time.sleep(2)
			
			# Verificar disponibilidad
			page_text = driver.page_source.lower()
			no_appointment_found = NO_APPOINTMENT_TEXT.lower() in page_text
			available = not no_appointment_found
			
			logging.info(f"¿'No hay citas disponibles' en página?: {no_appointment_found}")
			logging.info(f"¿Citas disponibles?: {available}")
			
			if available:
				message = f"✅ CITA DISPONIBLE\n\nHay cita disponible para {SERVICE_NAME} en Prenot@mi.\nRevisa inmediatamente: {booking_url}"
				send_telegram_message(message)
				logging.warning("⚠️ NOTIFICACIÓN DE CITA ENVIADA POR TELEGRAM")
				return True
			else:
				logging.info("✅ No hay citas disponibles en este momento")
				return False
				
		finally:
			driver.quit()
			
	except Exception as e:
		logging.error(f"❌ Error con navegador anti-detección: {type(e).__name__}: {e}")
		logging.info("No se puede verificar sin navegador real")
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
