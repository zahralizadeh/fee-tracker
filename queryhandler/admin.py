from django.contrib import admin
from .models import PropertyPredictResponse

# Register your models here.
class PropertyPredictResponseAdmin(admin.ModelAdmin):
    list_display = ['responseDate', 'offertype', 'location', 'area', 'price1', 'price2', 'rooms', 'age' ]
    search_fields = ['responseDate', 'offertype', 'location']

admin.site.register(PropertyPredictResponse, PropertyPredictResponseAdmin)