from django.contrib import admin
from .models import PropertyPredictResponse

# Register your models here.
class PropertyPredictResponseAdmin(admin.ModelAdmin):
    list_display = ['responseDate', 'offertype', 'location', 'area',  'rooms', 'age', 'price1', 'price2','recordcount']
    search_fields = ['responseDate', 'offertype', 'location']

admin.site.register(PropertyPredictResponse, PropertyPredictResponseAdmin)