from django.contrib import admin
from .models import User, Phone, Token

# Register your models here.
admin.site.register(User)
admin.site.register(Phone)
admin.site.register(Token)
