from django.contrib import admin
from .models import Token, activationcode


# Register your models here.
class TokenAdmin (admin.ModelAdmin):
    list_display = ['user', 'token']

class activationcodeAdmin (admin.ModelAdmin):
    list_display = ['username', 'email','code','time']

admin.site.register(Token, TokenAdmin)
admin.site.register(activationcode, activationcodeAdmin)