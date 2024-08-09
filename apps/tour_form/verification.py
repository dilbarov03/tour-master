import os
import random

import redis
from random import randint
from decouple import config
import requests

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

PLAY_MOBILE_URL = config('PLAY_MOBILE_URL')
PLAY_MOBILE_LOGIN = config('PLAY_MOBILE_LOGIN')
PLAY_MOBILE_PASSWORD = config('PLAY_MOBILE_PASSWORD')
redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def generate_code():
    return randint(100000, 999999)


def send_code(phone_number):
    if redis_connection.get(phone_number):
        return False, "Code already sent"

    code = generate_code()
    send_phone_notification(phone_number, code)
    print(f"Your code for number {phone_number} is {code}")

    redis_connection.set(phone_number, code)
    redis_connection.expire(phone_number, time=120)

    return True, "Code sent successfully"


def verify_code_cache(phone_number, code):
    data = redis_connection.get(phone_number)
    if not data:
        return False, "Code expired"
    stored_code = data.decode('utf-8')
    if stored_code == code:
        redis_connection.set(f"{phone_number}_verified", "True")
        redis_connection.expire(f"{phone_number}_verified", time=120)
        return True, "Code verified successfully"
    return False, "Code is incorrect"


def check_verification_status(phone_number):
    verified_phone = redis_connection.get(f"{phone_number}_verified")
    if not verified_phone:
        return False, "Phone number must be verified first"
    if verified_phone.decode('utf-8') != "True":
        return False, "Phone number is not verified"
    return True, "Phone number is verified"


def send_phone_notification(phone, code):
    payload = {
        "messages": [
            {
                "recipient": f"{phone}",
                "message-id": f"mock_exam_{random.randint(10000, 100000)}",
                "sms": {
                    "originator": "Mohirdev",
                    "content": {
                        "text": f"Salom! Sizning tasdiqlash kodingiz - {code}\n"
                    }
                }
            }
        ]
    }
    response = requests.post(PLAY_MOBILE_URL, json=payload, auth=(PLAY_MOBILE_LOGIN, PLAY_MOBILE_PASSWORD))
    return response.status_code
