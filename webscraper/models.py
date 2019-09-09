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
    
class Scrape(models.Model):
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    status = models.CharField(max_length = 20)
    resultnumber = models.IntegerField()
    scrapetype = models.CharField(max_length = 20) # for Rent / Sell
    site = models.CharField(max_length = 255)
    baselink = models.CharField(max_length = 255)
    currentlink = models.CharField(max_length = 255)
    pagenumber = models.IntegerField()
    pagetarget = models.IntegerField()
    currnetrecord = models.IntegerField()
    def __str__(self):
        return "{}-{}-{}".format(self.endTime,self.status,self.scrapetype)

    



#class ScrapeLink(models.Model):
  #  baselink = models.CharField(max_length = 255)
   # link = models.CharField(max_length = 255)
   # pagenumber = models.IntegerField()
    #pagetarget = models.IntegerField()
    #target = 
    



