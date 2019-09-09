from django.contrib import admin
from .models import Token, activationcode
# Register your models here.

admin.site.register(Token)
admin.site.register(activationcode)