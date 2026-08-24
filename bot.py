import logging
import os
import sys
import time

import requests


LOGIN_URL = "https://prenotami.esteri.it/Home/Login"
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))
NO_APPOINTMENT_TEXT = os.getenv("NO_APPOINTMENT_TEXT", "No hay citas disponibles")
SERVICE_NAME = os.getenv("SERVICE_NAME", "renovación de pasaporte")


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
	return NO_APPOINTMENT_TEXT not in response.text


def check_booking():
	email = required_setting("PRENOTAMI_EMAIL")
	password = required_setting("PRENOTAMI_PASSWORD")
	booking_url = required_setting("BOOKING_URL")

	with requests.Session() as session:
		response = session.post(
			LOGIN_URL,
			data={"Email": email, "Password": password},
			timeout=30,
		)
		response.raise_for_status()

		if booking_available(session, booking_url):
			send_telegram_message(
				f"Juan, hay cita disponible para {SERVICE_NAME} en Prenot@mi. Revisa el trámite."
			)
			return True
	return False


def main(run_once=False):
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s %(levelname)s %(message)s",
	)
	required_setting("PRENOTAMI_EMAIL")
	required_setting("PRENOTAMI_PASSWORD")
	required_setting("TELEGRAM_TOKEN")
	required_setting("CHAT_ID")
	required_setting("BOOKING_URL")

	while True:
		try:
			if check_booking():
				return
			logging.info("No hay citas disponibles; próxima revisión en %s segundos", CHECK_INTERVAL_SECONDS)
		except Exception:
			logging.exception("Error durante la revisión")
		if run_once:
			return
		time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
	main(run_once="--once" in sys.argv)
