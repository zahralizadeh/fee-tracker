from django.db import models

# Create your models here.
class PropertyFile(models.Model):
    offertype = models.CharField(max_length = 50)
    location = models.CharField(max_length = 255)
    area = models.IntegerField()
    price1 = models.BigIntegerField()
    price2 = models.BigIntegerField()
    rooms = models.IntegerField()
    age = models.IntegerField()
    def __str__(self):
        return "{}-{}-{} متری".format('فروش' if (self.offertype == '1') else 'اجاره', self.location,self.area)
