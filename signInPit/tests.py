from django.test import TestCase, Client
from django.urls import reverse

import json
import random


class SignUpTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_user(self):
        payload = {
            "firstName": "Unit",
            "lastName": "Test",
            "email": f"unittest{random.randint(1,1000000)}@test.com",
            "password": "admin",
            "phones": [
                {"number": random.randint(1, 1000000000), "area_code": 81, "country_code": "+55"}
            ],
        }

        response = self.client.post(reverse("signup"), payload)
        code = json.loads(response.content)["errorCode"]
        self.assertEqual(code, 200)

    def test_duplicated_email(self):
        email = (f"unittest{random.randint(1,1000000)}@test.com",)
        payload = {
            "firstName": "Unit",
            "lastName": "Test",
            "email": email,
            "password": "admin",
            "phones": [
                {"number": random.randint(1, 1000000000), "area_code": 81, "country_code": "+55"}
            ],
        }

        response = self.client.post(reverse("signup"), payload)
        self.assertEqual(response.status_code, 200)

        payload = {
            "firstName": "Unit",
            "lastName": "Test",
            "email": email,
            "password": "admin",
            "phones": [
                {"number": random.randint(1, 1000000000), "area_code": 81, "country_code": "+55"}
            ],
        }
        response = self.client.post(reverse("signup"), payload)
        code = json.loads(response.content)["errorCode"]
        self.assertEqual(code, 409)

    def test_duplicated_phone(self):
        phone = (random.randint(1, 100000000),)
        payload = {
            "firstName": "Unit",
            "lastName": "Test",
            "email": f"unittest{random.randint(1,1000000)}@test.com",
            "password": "admin",
            "phones": [{"number": phone, "area_code": 81, "country_code": "+55"}],
        }

        response = self.client.post(reverse("signup"), payload)
        self.assertEqual(response.status_code, 200)

        payload = {
            "firstName": "Unit",
            "lastName": "Test",
            "email": f"unittest{random.randint(1,1000000)}@test.com",
            "password": "admin",
            "phones": [{"number": phone, "area_code": 81, "country_code": "+55"}],
        }
        response = self.client.post(reverse("signup"), payload)
        code = json.loads(response.content)["errorCode"]
        self.assertEqual(code, 409)

    def test_missing_fields(self):
        payload = {
            "firstName": "Unit",
            "email": f"unittest{random.randint(1,1000000)}@test.com",
            "password": "admin",
            "phones": [
                {"number": random.randint(1, 1000000000), "area_code": 81, "country_code": "+55"}
            ],
        }

        response = self.client.post(reverse("signup"), payload)
        code = json.loads(response.content)["errorCode"]
        self.assertEqual(code, 400)


class SignInTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_successful_login(self):
        email = (f"unittest{random.randint(1,1000000)}@test.com",)
        payload = {
            "firstName": "Unit",
            "lastName": "Test",
            "email": f"unittest{random.randint(1,1000000)}@test.com",
            "password": "admin",
            "phones": [
                {"number": random.randint(1, 1000000000), "area_code": 81, "country_code": "+55"}
            ],
        }

        response = self.client.post(reverse("signup"), payload)
        self.assertEqual(response.status_code, 200)

        payload = {"email": email, "password": "admin"}
        response = self.client.post(reverse("signin"), payload)
        self.assertEqual(response.status_code, 200)

    def test_incorrect_password(self):
        email = (f"unittest{random.randint(1,1000000)}@test.com",)
        payload = {
            "firstName": "Unit",
            "lastName": "Test",
            "email": f"unittest{random.randint(1,1000000)}@test.com",
            "password": "admin",
            "phones": [
                {"number": random.randint(1, 1000000000), "area_code": 81, "country_code": "+55"}
            ],
        }

        response = self.client.post(reverse("signup"), payload)
        self.assertEqual(response.status_code, 200)

        payload = {"email": email, "password": "not admin"}
        response = self.client.post(reverse("signin"), payload)
        code = json.loads(response.content)["errorCode"]
        self.assertEqual(code, 401)

    def test_missing_fields(self):
        email = (f"unittest{random.randint(1,1000000)}@test.com",)

        payload = {"email": email}
        response = self.client.post(reverse("signin"), payload)
        code = json.loads(response.content)["errorCode"]
        self.assertEqual(code, 400)

    def test_unregistered_email(self):
        email = (f"unittest{random.randint(1,1000000)}@test.com",)

        payload = {"email": email, "password": "admin"}
        response = self.client.post(reverse("signin"), payload)
        code = json.loads(response.content)["errorCode"]
        self.assertEqual(code, 401)


class MeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_token(self):
        email = (f"unittest{random.randint(1,1000000)}@test.com",)
        payload = {
            "firstName": "Unit",
            "lastName": "Test",
            "email": f"unittest{random.randint(1,1000000)}@test.com",
            "password": "admin",
            "phones": [
                {"number": random.randint(1, 1000000000), "area_code": 81, "country_code": "+55"}
            ],
        }

        response = self.client.post(reverse("signup"), payload)
        self.assertEqual(response.status_code, 200)

        token = json.loads(response.content)["token"]
        headers = {"Authorization": token}

        response = self.client.get(reverse("me"), headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_invalid_token(self):
        headers = {"Authorization": "123"}

        response = self.client.get(reverse("me"), headers=headers)
        code = json.loads(response.content)["errorCode"]
        self.assertEqual(code, 401)
