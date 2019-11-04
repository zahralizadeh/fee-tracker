
import csv
from io import BytesIO
import xlsxwriter
from django.http import HttpResponse
from django.contrib import admin
from .models import PropertyFile, Scrape
from django.core.exceptions import PermissionDenied
#from django.contrib.admin.util import label_for_field


def export_xsl(modeladmin, request, queryset):
    # create our spreadsheet.  I will create it in memory with a StringIO
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'offertype')
    worksheet.write('B1', 'location')
    worksheet.write('C1', 'area')
    worksheet.write('D1', 'price')
    worksheet.write('E1', 'rooms')
    worksheet.write('F1', 'age')
    worksheet.write('G1', 'propertytype')
    i = 2

    for obj in queryset:
        worksheet.write('A'+str(i), str(obj.offertype))
        worksheet.write('B'+str(i), obj.location)
        worksheet.write('C'+str(i), str(obj.area))
        worksheet.write('D'+str(i), str(obj.price))
        worksheet.write('E'+str(i), str(obj.rooms))
        worksheet.write('F'+str(i), str(obj.age))
        worksheet.write('G'+str(i), obj.propertytype)
        i += 1    
    workbook.close()
    output.seek(0)

    # create a response
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="feetracker_objs.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response
export_xsl.short_description = "Export selected as xsl"

def download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
download_csv.short_description = "Download selected as csv"


# Register your models here.
class PropertyFileAdmin (admin.ModelAdmin):
    list_display = ['offertype', 'location', 'area', 'price', 'rooms', 'age', 'publishdate', 'propertytype']
    search_fields = ('offertype', 'location','propertytype' )
    list_filter = ('offertype', 'propertytype' ,'location')
    actions = [download_csv,export_xsl]

    
class ScrapeAdmin (admin.ModelAdmin):
    list_display = ['endTime','status', 'scrapetype', 'propertytype', 'currnetrecord','pagenumber','last_update_time', 'site']
    search_fields = ('last_update_time', 'status', 'scrapetype','propertytype' )
    

admin.site.register(PropertyFile,PropertyFileAdmin)
admin.site.register(Scrape,ScrapeAdmin)

