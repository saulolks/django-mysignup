from django.test import TestCase, Client
from django.url import reverse

import random


class SignUpTest(TestCase):
    def create_user_test(self):
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

    def duplicated_email_test(self):
        email = f"unittest{random.randint(1,1000000)}@test.com",
        payload = {
            "firstName": "Unit",
            "lastName": "Test",
            "email": email
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
            "email": email
            "password": "admin",
            "phones": [
                {"number": random.randint(1, 1000000000), "area_code": 81, "country_code": "+55"}
            ],
        }
        response = self.client.post(reverse("signup"), payload)
        self.assertEqual(response.status_code, 409)


    def duplicated_phone_test(self):
        phone = random.randint(1,100000000),
        payload = {
            "firstName": "Unit",
            "lastName": "Test",
            "email": f"unittest{random.randint(1,1000000)}@test.com",
            "password": "admin",
            "phones": [
                {"number": phone, "area_code": 81, "country_code": "+55"}
            ],
        }

        response = self.client.post(reverse("signup"), payload)
        self.assertEqual(response.status_code, 200)

        payload = {
            "firstName": "Unit",
            "lastName": "Test",
            "email": f"unittest{random.randint(1,1000000)}@test.com",
            "password": "admin",
            "phones": [
                {"number": phone, "area_code": 81, "country_code": "+55"}
            ],
        }
        response = self.client.post(reverse("signup"), payload)
        self.assertEqual(response.status_code, 409)

    def missing_fields_test(self):
        pass


class SignInTest(TestCase):
    def successful_login_test(self):
        pass

    def incorrect_password_test(self):
        pass

    def missing_fields_test(self):
        pass


class MeTest(TestCase):
    def invalid_token_test(self):
        pass

    def anothers_token_test(self):
        pass