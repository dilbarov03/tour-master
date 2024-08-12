from .base import *  # noqa

###################################################################
# General
###################################################################

DEBUG = True

###################################################################
# Django security
###################################################################

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = [
    "https://63f7-62-169-31-254.ngrok-free.app/",
    "http://62.169.31.254/"
]


###################################################################
# CORS
###################################################################

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]


