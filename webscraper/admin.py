from django.contrib import admin
from .models import PropertyFile, Scrape

# Register your models here.
class PropertyFileAdmin (admin.ModelAdmin):
    list_display = ['offertype', 'location', 'area', 'price1', 'price2', 'rooms', 'age', 'publishdate' ]
    search_fields = ('offertype', 'location' )

class ScrapeAdmin (admin.ModelAdmin):
    list_display = ['endTime','status', 'scrapetype', 'currnetrecord','pagenumber','last_update_time', 'site']
    search_fields = ('last_update_time', 'status', 'scrapetype' )
    

admin.site.register(PropertyFile,PropertyFileAdmin)
admin.site.register(Scrape,ScrapeAdmin)

