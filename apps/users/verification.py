import os
from random import randint
import requests

from django.core.cache import cache
from dotenv import load_dotenv, set_key

load_dotenv()


def generate_code():
    return randint(100000, 999999)


# def refresh_token():
#     url = 'https://notify.eskiz.uz/api/auth/refresh'
#
#     current_token = os.getenv("SMS_TOKEN")
#     headers = {
#         "Authorization": f"Bearer {current_token}",
#     }
#
#     response = requests.patch(url, headers=headers)
#
#     if response.status_code == 200:
#         new_token = response.json()['token']
#
#         # Update the .env file with the new token
#         set_key('.env', 'SMS_TOKEN', new_token)
#
#         return new_token
#     else:
#         raise Exception(f"Failed to refresh token, status code: {response.status_code}, response: {response.text}")


def get_new_token():
    url = 'https://notify.eskiz.uz/api/auth/login'

    request_body = {
        "email": os.getenv("SMS_EMAIL"),
        "password": os.getenv("SMS_PASSWORD")
    }

    response = requests.post(url, json=request_body)

    if response.status_code == 200:
        token = response.json()['data']['token']
        set_key('.env', 'SMS_TOKEN', token)
        return token
    else:
        raise Exception(f"Failed to get new token, status code: {response.status_code}, response: {response.text}")

def send_code(phone_number):
    if cache.get(phone_number):
        return False, "Code already sent"

    code = generate_code()
    send_sms(phone_number, code)
    print(f"Your code for number {phone_number} is {code}")

    cache.set(phone_number, code, timeout=120)

    return True, f"Code sent successfully"


def verify_code_cache(phone_number, code):
    stored_code = cache.get(phone_number)
    print(stored_code, code)
    print(type(stored_code), type(code))
    if not stored_code:
        return False, "Code expired"
    if stored_code == code:
        cache.set(f"{phone_number}_verified", "True", timeout=120)
        return True, "Code verified successfully"
    return False, "Code is incorrect"


def check_verification_status(phone_number):
    verified_phone = cache.get(f"{phone_number}_verified")
    if not verified_phone:
        return False, "Phone number must be verified first"
    if verified_phone != "True":
        return False, "Phone number is not verified"
    return True, "Phone number is verified"


def send_sms(phone="998972081018", code=111111):
    url = 'https://notify.eskiz.uz/api/message/sms/send/'

    token = os.getenv("SMS_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    message = f"Travel-savol.uz saytidagi buyurtmani tasdiqlash uchun kod: {code}"

    data = {
        'mobile_phone': phone,
        'message': message,
        'from': '4546',
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 401:
        token = get_new_token()
        headers["Authorization"] = f"Bearer {token}"
        response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": f"Failed to send SMS, status code: {response.status_code}",
            "response": response.text
        }


def eskiz_test():
    url = 'https://notify.eskiz.uz/api/message/sms/send'

    token = os.getenv("SMS_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    phone = "998972081018"
    data = {
        'mobile_phone': phone,
        'message': "eskiz test",
        'from': '4546',

    }

    response = requests.post(url, headers=headers, data=data)
    print(response.text)
    print(response.status_code)
