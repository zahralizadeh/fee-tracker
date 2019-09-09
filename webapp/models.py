from django.db import models
from django.contrib.auth.models import User


# Create your models here.
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
    def __str__(self):
        return "{}".format(self.username)



