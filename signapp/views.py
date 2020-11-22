import json
import hashlib
import uuid

from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from .models import User, Phone, Token
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from .utils import jwt_manager
from .utils.exceptions import (
    EmailAlreadyExistsError,
    EmailNotFoundError,
    IncorrectPasswordError,
    InvalidTokenError,
    ExpiredTokenError,
)
from django.db import IntegrityError
from django.db import transaction

# Create your views here.


@api_view(["POST"])
@csrf_exempt
def signup(request):
    payload = request.data
    try:
        print(payload)
        password = hashlib.sha256(payload["password"].encode()).hexdigest()

        try:
            user = User.objects.get(email=payload["email"])
        except Exception as ex:
            user = None

        if user:
            raise EmailAlreadyExistsError

        user = User(
            firstname=payload["firstName"],
            lastname=payload["lastName"],
            email=payload["email"],
            password=password,
        )

        phone_list = []
        for item in payload["phones"]:
            phone = Phone(
                number=item["number"],
                area_code=item["area_code"],
                country_code=item["country_code"],
                user=user,
            )
            phone_list.append(phone)

        token = Token(user=user)
        with transaction.atomic():
            user.save()
            [phone.save() for phone in phone_list]
            token.save()

        jwt = jwt_manager.get(user.id, token.hash)

        return JsonResponse({"token": jwt, "statusCode": 200})
    except KeyError:
        print("[ERROR] Missing fields")
        return JsonResponse({"message": "Missing fields", "errorCode": 400})
    except EmailAlreadyExistsError:
        print("[ERROR] Email already exists in database")
        return JsonResponse({"message": "E-mail already exists", "errorCode": 409})
    except IntegrityError:
        print("[ERROR] Phone is already registered")
        return JsonResponse({"message": "Phone is already registered", "errorCode": 409})
    except Exception as ex:
        print("[ERROR] Unknown error:", ex)
        return JsonResponse({"message": "Server error", "errorCode": 400})


@api_view(["POST"])
@csrf_exempt
def signin(request):
    payload = request.data
    try:
        email = payload["email"]
        password = hashlib.sha256(payload["password"].encode()).hexdigest()

        try:
            user = User.objects.get(email=payload["email"])
        except Exception as ex:
            user = None

        if not user:
            raise EmailNotFoundError

        if password != user.password:
            raise IncorrectPasswordError

        user.update_login()
        token = Token.objects.get(user=user)
        token.update_hash()

        with transaction.atomic():
            user.save()
            token.save()

        jwt = jwt_manager.get(user.id, token.hash)
        return JsonResponse({"token": jwt, "statusCode": 200})
    except KeyError:
        print("[ERROR] Missing fields")
        return JsonResponse({"message": "Missing fields", "errorCode": 400})
    except EmailNotFoundError:
        print("[ERROR] Email not found")
        return JsonResponse({"message": "Invalid e-mail or password", "errorCode": 401})
    except IncorrectPasswordError:
        print("[ERROR] Incorrect password")
        return JsonResponse({"message": "Invalid e-mail or password", "errorCode": 401})
    except Exception as ex:
        print("[ERROR] Unknown error:", ex)
        return JsonResponse({"message": "Server error", "errorCode": 400})


@api_view(["GET"])
@csrf_exempt
def me(request):
    try:
        authorization = request.headers["Authorization"]

        user_id, token = jwt_manager.validate(authorization)

        try:
            token = Token.objects.get(hash=token)

            if token.user.id != user_id:
                raise InvalidTokenError
        except Exception as ex:
            raise InvalidTokenError

        if token.is_expired():
            raise ExpiredTokenError

        serializer = UserSerializer(token.user)
        return JsonResponse({"data": serializer.data, "statusCode": 200})
    except KeyError:
        print("[ERROR] Missing fields")
        return JsonResponse({"message": "Unauthorized", "errorCode": 401})
    except ExpiredTokenError:
        print("[ERROR] Expired token error")
        return JsonResponse({"message": "Expired token", "errorCode": 401})
    except InvalidTokenError:
        print("[ERROR] Invalid token error")
        return JsonResponse({"message": "Unauthorized", "errorCode": 401})
    except Exception as ex:
        print("[ERROR] Unknown error:", ex)
        return JsonResponse({"message": "Server error", "errorCode": 400})