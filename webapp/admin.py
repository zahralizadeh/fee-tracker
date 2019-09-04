from django.contrib import admin
from .models import PropertyFile, Token, activationcode
# Register your models here.

admin.site.register(PropertyFile)
admin.site.register(Token)
admin.site.register(activationcode)