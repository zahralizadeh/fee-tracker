import logging
import numpy as np
from sklearn import tree
from json import JSONEncoder
from django.db import models
from datetime import datetime
from webscraper.models import PropertyFile
from django.http import JsonResponse
from django.utils import timezone


 
logger = logging.getLogger(__name__)

# Create your models here.
class PropertyPredictResponse(models.Model):
    offertype = models.IntegerField()               # From user
    location = models.CharField(max_length = 255)   # From user
    area = models.IntegerField()                    # From user
    rooms = models.IntegerField()                   # From user
    age = models.IntegerField()                     # From user
    price1 = models.BigIntegerField()               # Prediction result
    price2 = models.BigIntegerField()               # Prediction result
    responseDate = models.DateTimeField()           # Date of request
    firstdata = models.DateTimeField()              # PublishDate of first property in database
    lastdata = models.DateTimeField()               # PublishDate of last property in database
    filtering = models.CharField(max_length=50)     # Criterias which filter is applied to
    recordcount = models.IntegerField()             # Number of filtered recorded

    def predict (self):
    #TODO: token provided or something to prevent robots
    #TODO: prediction model. save result of prediction
        self.responseDate = timezone.make_aware(datetime.now())
        data = PropertyFile.objects.filter(\
            offertype=self.offertype,\
            location__contains=self.location,\
            area__range=(self.area-10,self.area+10),\
            rooms=self.rooms,\
            age__range=(self.age-3 if self.age>3 else 0,self.age+3)).order_by('-publishdate')

        self.filtering = 'offertype location area rooms age'
        if data.count()< 50:
            data = PropertyFile.objects.filter(\
                offertype=self.offertype,\
                location__contains=self.location,\
                rooms=self.rooms,\
                age__range=(self.age-3 if self.age>3 else 0,self.age+3)).order_by('-publishdate')
            self.filtering = 'offertype location rooms age'

            if data.count()< 50:
                data = PropertyFile.objects.filter(\
                    offertype=self.offertype,\
                    location__contains=self.location,\
                    rooms=self.rooms).order_by('-publishdate')
                self.filtering = 'offertype location rooms'

                if data.count()< 50:
                    data = PropertyFile.objects.filter(\
                        offertype=self.offertype,\
                        location__contains=self.location).order_by('-publishdate')
                    self.filtering = 'offertype location'
                    if data.count()< 50:
                        self.filtering = 'not enough data'
                        #TODO: recheck
                        return JsonResponse({
                            'message': 'There is not enogh data for this location',
                            }, encoder=JSONEncoder)

        self.recordcount = data.count() if data.count()<150 else 150  # max 150 recordes are needed for prediction
        x = []
        y = []
        if self.offertype == '1':   # load input and output lists for prediction with last 150 record in database( MAX)
            for j in range(0, self.recordcount):
                x.append([data[j].area, data[j].rooms,data[j].age])
                y.append(data[j].price1)
        elif self.offertype == '2':
            for j in range(0, self.recordcount):
                x.append([data[j].area, data[j].rooms,data[j].age])
                y.append([data[j].price1,data[j].price2])
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(x,y)
        answer = clf.predict([[self.area,self.rooms,self.age]])
        
        self.firstdata = data[0].publishdate
        self.lastdata = data[self.recordcount-1].publishdate
        
        if self.offertype == '1':
            self.price1 = answer[0]
            self.price2 = 0
            return JsonResponse({
                'firstdata': ' %s'%self.firstdata,
                'lastdata': ' %s'%self.lastdata,
                'filter' : self.filtering,
                'count' : '%i'%self.recordcount,
                'answer': 'I predict its cost as %i tomans'%self.price1,
                }, encoder=JSONEncoder)
        else:
            self.price1 = answer[0][1]
            self.price2 = answer[0][0]
            return JsonResponse({
                'firstdata': ' %s'%self.firstdata,
                'lastdata': ' %s'%self.lastdata,
                'filter' : self.filtering,
                'count' : '%i'%self.recordcount,
                'answer': 'I predict its cost as %i tomans for deposit and %i tomans as monthly rent'%(answer[0][1],answer[0][0]),
                }, encoder=JSONEncoder)
        logger.debug('New response saved in database in %s'%self.responseDate)
    
    def save(self, *args,**kwargs):
        self.full_clean()
        super(PropertyPredictResponse, self).save(*args, **kwargs)
