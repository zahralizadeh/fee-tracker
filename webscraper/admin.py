from django.contrib import admin
from .models import PropertyFile, ScrapeLog

# Register your models here.
admin.site.register(PropertyFile)
admin.site.register(ScrapeLog)

