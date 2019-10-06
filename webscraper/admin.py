from django.contrib import admin
from .models import PropertyFile, Scrape

# Register your models here.
class PropertyFileAdmin (admin.ModelAdmin):
    list_display = ['offertype', 'location', 'area', 'price', 'rooms', 'age', 'publishdate', 'propertytype']
    search_fields = ('offertype', 'location','propertytype' )

class ScrapeAdmin (admin.ModelAdmin):
    list_display = ['endTime','status', 'scrapetype', 'propertytype', 'currnetrecord','pagenumber','last_update_time', 'site']
    search_fields = ('last_update_time', 'status', 'scrapetype','propertytype' )
    

admin.site.register(PropertyFile,PropertyFileAdmin)
admin.site.register(Scrape,ScrapeAdmin)

