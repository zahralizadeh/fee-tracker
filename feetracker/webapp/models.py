from django.db import models
from django.contrib.auth.models import User


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

class Token(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    token = models.CharField(max_length = 48)
    def __str__(self):
        return "{}-token".format(self.user)

class activationcode(models.Model):
    username = models.CharField(max_length = 50)
    email = models.CharField(max_length = 120)
    password = models.CharField(max_length = 50)
    code = models.CharField(max_length = 28)
    time = models.DateTimeField()



