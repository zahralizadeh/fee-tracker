import re
import logging
import requests
from bs4 import BeautifulSoup
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
        return "{}-{}-{} متری".format(self.offertype, self.location,self.area)
    
class Scrape(models.Model):
    logger = logging.getLogger(__name__)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    status = models.CharField(max_length = 20)
    resultnumber = models.IntegerField()
    scrapetype = models.CharField(max_length = 20)  # for Rent / Sell
    site = models.CharField(max_length = 255)   #site title for scraping
    baselink = models.CharField(max_length = 255)
    currentlink = models.CharField(max_length = 255)
    pagenumber = models.IntegerField()      #number of last web page that is checked
    pagetarget = models.IntegerField()  
    currnetrecord = models.IntegerField()   #number of records saved in database successfully
    num_target_records = 47,496   #TODO: change the logic for end of process  #target number of records that should be saved in database  
    
    def __str__(self):
        return "{}-{}-{}".format(self.endTime,self.status,self.scrapetype)

    def startscraping(self):    
        #while self.pagenumber <= self.pagetarget:
            self.buildlink()
            page = requests.get(self.currentlink, verify=False)
            soup = BeautifulSoup(page.text,'html.parser') 
            self.logger.debug('----def models.scrape.startscraping  -----> pagenumber: %i'%(self.pagenumber))
            if self.pagenumber == 1:
                self.getTargetPageNumber(soup)
            all_files = soup.find_all('li', class_ =re.compile('blocks'))
            #extract each file and save it in the database
            for file in all_files:
                if(self.savePropertyFile(self.get_location(file),self.get_area(file),self.get_price(file),\
                    self.get_rooms(file),self.get_building_age(file)) == True):
                    self.currnetrecord += 1
            self.pagenumber += 1

    def buildlink(self):
        self.baselink = 'https://www.%s.ir/%s/املاک/تهران/'%(self.site,self.scrapetype)
        if self.pagenumber > 1:
            self.currentlink = self.baselink + '/%i/'%(self.pagenumber)
        else:
            self.currentlink = self.baselink
        self.logger.debug('----def models.scrape.startscraping  -----> link: '+self.currentlink)


            
    def getTargetPageNumber(self,soup):
        records_info = soup.find('div',class_='right pg_counts').get_text(strip=True).replace(',','').split()
        self.logger.debug('----def models.scrape.firstpage  -----> records_info: %s'%(records_info))
        record_num = 0
        try:
            record_num = int(records_info[2].strip())
            self.pagetarget = int(record_num/24)
            if (record_num%24) > 0:
                self.pagetarget += 1
            self.logger.debug('----def models.scrape.firstpage  -----> pagetarget:%i'%(self.pagetarget))
        except:
            self.logger.debug('----def models.scrape.firstpage  ----->  Exception in calculating target page')
            self.status = 'error'                
        
    def savePropertyFile (self,location,area,price,rooms,age):
        self.logger.debug('----def models.scrape.savePropertyFile  -----> location:%s'%(location))
        self.logger.debug('----def models.scrape.savePropertyFile  -----> area:%s'%(area))
        self.logger.debug('----def models.scrape.savePropertyFile  -----> price:%s'%(price[0]))
        self.logger.debug('----def models.scrape.savePropertyFile  -----> rooms:%s'%(rooms))
        self.logger.debug('----def models.scrape.savePropertyFile  -----> age:%s'%(age))

        if self.scrapetype == 'خرید-فروش':   #save data in database for BUY cases
            if price[0] > 0 and rooms > 0 and area > 0:
                #thisFile = PropertyFile.objects.create(\
                #    offertype = self.scrapetype,\
                #    location = location,\
                 #   area = area,\
                 #   price1 = price[0],\
                 #   price2 = 0,\
                 #   rooms = rooms,\
                 #   age = age)
                this_file = PropertyFile(offertype = self.scrapetype,location = location,area = area,\
                    price1 = price[0], price2 = 0,rooms = rooms,age = age )
                this_file.save()
                #thisFile = PropertyFile(self.scrapetype,location,area,price[0],0,rooms,age)
                #thisFile.save()                
                return(True)
            return(False)
        elif self.scrapetype == 'رهن-اجاره': #save data in database for RENT cases
            if price == [0,0] or rooms == 0 or area == 0:  #means data is not valid and usefull 
                return(False)
            else:
                thisFile = PropertyFile(self.scrapetype,location,area,price[0],price[1],rooms,age)
                thisFile.save() 
                return(True)

    def get_location(self,file):
        return file.find('div',class_='location').span.extract().get_text(strip=True)

    def get_area(self,file):
        try:
            area_str =  file.find('i',class_ = 'ihome-arrows').next_sibling.replace(' متر مربع','').strip()
            return int(area_str.replace(',',''))
        except:
            return 0
        
    def get_price(self,file):
        price = [] 
        if self.scrapetype == 'خرید-فروش':     #extract price for BUY cases
            p = file.find('div',class_ = 'price')
            try:
                p.span.extract()
                price_str = p.get_text(strip = True).replace(',','').replace('تومان','')
                price.append(int(price_str))    
            except:
                price.append(0)
        if self.scrapetype == 'رهن-اجاره':     #extract price for RENT cases
            p = file.find_all('div',attrs = {'class':['deposit','price']})
            if len(p)>1:        #it means that there is two prices including rent and deposit
                for q in p:
                    try:
                        q.span.extract()
                        price_str = q.get_text(strip = True).replace(',','').replace('تومان','')
                        price.append(int(price_str))    
                    except:
                        price.append(0)
            else:               #it means that there is one price, so the property is for full deposit
                price.append(0)
                try:
                    p[0].span.extract()
                    price_str = p[0].get_text(strip = True).replace(',','').replace('تومان','')
                    price.append(int(price_str))    
                except:
                    price.append(0)       
        return price
        
    def get_rooms(self,file):
        try:
            rooms_str =  file.find('i',class_ = 'ihome-bed').next_sibling.strip()
            return int(rooms_str)
        except:
            return 0
        
    def get_building_age(self,file):
        try:
            age_str =  file.find('i',class_ = 'ihome-building-age').next_sibling.replace('سن بنا','').strip()
            return int(age_str.replace(',',''))
        except:
            return 0



#class ScrapeLink(models.Model):
  #  baselink = models.CharField(max_length = 255)
   # link = models.CharField(max_length = 255)
   # pagenumber = models.IntegerField()
    #pagetarget = models.IntegerField()
    #target = 
    



