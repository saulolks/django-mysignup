import jwt
import os
from .exceptions import InvalidTokenError
from django.conf import settings


def get(user, token):
    secret = settings.SECRET_KEY
    payload = {"user": user, "token": str(token)}
    return jwt.encode(payload, secret, algorithm="HS256").decode("UTF-8")


def validate(token):
    try:
        secret = settings.SECRET_KEY
        payload = jwt.decode(jwt=token, key=secret, algorithms=["HS256"])
        return payload["user"], payload["token"]
    except Exception as ex:
        raise InvalidTokenError
