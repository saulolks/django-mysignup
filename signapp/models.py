import uuid
import pytz

from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    def update_login(self):
        self.last_login = timezone.now()

    def __str__(self):
        return "%d - %s %s - %s" % (self.id, self.firstname, self.lastname, self.email)


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(unique=False)
    area_code = models.IntegerField(unique=False)
    country_code = models.CharField(max_length=5, unique=False)
    user = models.ForeignKey("user", on_delete=models.CASCADE, related_name="phones")

    class Meta:
        unique_together = ("number", "area_code", "country_code")

    def __str__(self):
        return "%s %d%d" % (self.country_code, self.area_code, self.number)


class Token(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("user", on_delete=models.CASCADE, related_name="token")
    hash = models.CharField(default=str(uuid.uuid4()), editable=True, unique=True, max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def update_hash(self):
        self.hash = str(uuid.uuid4())

    def is_expired(self):
        timediff = timezone.now() - self.timestamp
        return timediff.total_seconds() > settings.TOKEN_EXPIRATION_SECONDS