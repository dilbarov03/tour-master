import os
from decimal import Decimal
from pathlib import Path

import environ
import requests
import asyncio
import websockets
from openpyxl.styles.builtins import output

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

BASE_URL = env.str("BASE_URL")


def send_telegram_message(text="Text", branch=None):
    token = env.str("BOT_TOKEN")

    if branch and branch.name == "Maxsus":
        chat_id = "-1002329450762"
    else:
        chat_id = env.str("CHAT_ID")

    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=html".format(token, chat_id, text)
    requests.post(url)
    return


def send_booking_message(booking):
    text = (
        f"<b>Tayyor tur paketlar</b>\n\n"
        f"<b>Zayavka ID:</b> {booking.id}\n"
        f"<b>Tur nomi:</b> {booking.tour.name}\n"
        f"<b>Jo'nab ketish davri:</b> {booking.tour.start_date}\n"
        f"<b>Mijoz FISH:</b> {booking.full_name}\n"
        f"<b>Mijoz telefon raqami:</b> {booking.phone}\n"
        f"<b>Mijoz telegram niki:</b> {booking.tg_username}\n"
        f"<b>Hudud:</b> {booking.region.name if booking.region else ''}\n"
        f"<b>Filial:</b> {booking.branch.name if booking.branch else ''}\n"
        f"<b>Sotuvchi:</b> {booking.user.full_name}\n\n"
        f"<b>Link:</b> {BASE_URL}/admin/tour_catalog/userbooking/{booking.id}/change/\n"
    )

    send_telegram_message(text, booking.branch)
    return


def send_form_message(form):
    text = (
        f"<b>Teriladigan tur paketlar</b>\n\n"
        f"<b>Zayavka ID:</b> {form.id}\n"
        f"<b>Davlati:</b> {form.country.name}\n"
        f"<b>Shahri:</b> {form.city.name}\n"
        f"<b>Jo'nab ketish davri:</b> {form.from_date}-{form.to_date}\n"
        f"<b>Sayohatchilar:</b> {form.get_people()}\n"
        f"<b>Mijoz FISH:</b> {form.full_name}\n"
        f"<b>Mijoz telefon raqami:</b> {form.phone}\n"
        f"<b>Hudud:</b> {form.region.name if form.region else ''}\n"
        f"<b>Filial:</b> {form.branch.name if form.branch else ''}\n"
        f"<b>Sotuvchi:</b> {form.user.full_name}\n\n"
        f"<b>Link:</b> {BASE_URL}/admin/tour_form/tourform/{form.id}/change/\n"
    )

    send_telegram_message(text, form.branch)
    return


async def listen():
    uri = "ws://localhost:8000/ws/notifications/1/"  # replace with your user_id
    async with websockets.connect(uri) as websocket:
        print(f"Connected to {uri}")
        while True:
            message = await websocket.recv()
            print(f"< {message}")


# asyncio.run(listen())

# round to nearest ten thousand
def round_up(number):
    remainder = number % 10000

    if remainder == 0:
        return number

    return number + (10000 - remainder)
