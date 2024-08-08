import os
from pathlib import Path

import environ
import requests

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

BASE_URL = env.str("BASE_URL")


def send_telegram_message(text="Text"):
    token = env.str("BOT_TOKEN")
    chat_id = env.str("CHAT_ID")

    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=html".format(token, chat_id, text)
    requests.post(url)
    return


def send_booking_message(booking):
    text = f'<b>Бронирование тура -</b> {booking.tour.name}\n\n'
    text += f'<b>ФИО:</b> {booking.full_name}\n'
    text += f'<b>Телефон:</b> {booking.phone}\n'
    text += f'<b>Username в Telegram:</b> {booking.tg_username}\n'
    text += f'<b>Общая стоимость:</b> {booking.total_price}\n\n'
    text += f'<b>Ссылка:</b> {BASE_URL}/admin/tour_catalog/userbooking/{booking.id}/change/\ngoogle.com'

    send_telegram_message(text)
    return
