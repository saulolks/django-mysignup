from rest_framework import serializers
from .models import User, Phone


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ["number", "area_code", "country_code"]


class UserSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True)

    class Meta:
        model = User
        fields = ["firstname", "lastname", "email", "created_at", "last_login", "phones"]
