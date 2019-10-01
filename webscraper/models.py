import re
import logging
import requests
from bs4 import BeautifulSoup
from django.db import models
from datetime import datetime, timedelta
from django.utils.timezone import make_aware



# Create your models here.
class PropertyFile(models.Model):
    offertype = models.IntegerField()
    location = models.CharField(max_length = 255)
    area = models.IntegerField()
    price = models.BigIntegerField()
    rooms = models.IntegerField()
    age = models.IntegerField()
    publishdate = models.DateTimeField()
    def __str__(self):
        return "{}-{}-{} متری".format(self.offertype, self.location,self.area)
    
class Scrape(models.Model):
    logger = logging.getLogger(__name__)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    last_update_time = models.DateTimeField()   # time treshhold of last update
    status = models.CharField(max_length = 20 , default= 'initialied')
    scrapetype = models.CharField(max_length = 20)  # for Rent / Sell
    site = models.CharField(max_length = 255, default = 'ihome')   #site title for scraping
    baselink = models.CharField(max_length = 255)
    currentlink = models.CharField(max_length = 255)
    pagenumber = models.IntegerField(default=1)      #number of last web page that is checked
    pagetarget = models.IntegerField(default=1)  
    currnetrecord = models.IntegerField(default=0)   #number of records saved in database successfully
    num_target_records = 47,496   

    def startscraping_update(self):  
        self.logger.debug("----def startscraping_update, Due Date is  ----->  %s"%(self.last_update_time))
        
        self.startTime = make_aware(datetime.now())
        self.logger.debug("----def startscraping_update, self.startTime  ----->  %s"%(self.startTime))

        self.status='initialied'
        last_property_time = make_aware(datetime.now())
        self.logger.debug("----def startscraping_update, last_property_time  ----->  %s"%(last_property_time))

        while (self.pagenumber <= self.pagetarget) and (last_property_time >= self.last_update_time):
            #TODO: ihome sort on date is not accurate
            self.buildlink()
            try:
                page = requests.get(self.currentlink, verify=False)
                soup = BeautifulSoup(page.text,'html.parser') 
                self.logger.debug('----def models.scrape.startscraping  -----> pagenumber: %i'%(self.pagenumber))
                if self.pagenumber == 1:    #in first page, calculate number of pages
                    self.getTargetPageNumber(soup)
                all_files = soup.find_all('li', class_ =re.compile('blocks'))
                #extract each file and save it in the database
                for file in all_files:
                    result = self.savePropertyFile(self.get_location(file),self.get_area(file),self.get_price(file),\
                        self.get_rooms(file),self.get_building_age(file),self.calculate_date(self.get_date(file)))
                    if result[0]== True:    #if file saved successfully .... 
                        self.currnetrecord += 1
                        last_property_time = result[1]  # publish date of file will be recorded in last_property_time
                self.logger.debug('----def models.scrape.startscraping  -----> last_property_time: %s'%(last_property_time))
            except:
                self.status = 'error in reading page %i'%self.pagenumber
            self.pagenumber = self.pagenumber + 1  #this page in scraped, go to next page
                
        #scraping is finished, finalize the scrape log and save it in database
        try:
            self.logger.debug('----startscraping  -----> end of scraping. number of saved records: %i'%(self.currnetrecord))
            self.endTime = make_aware(datetime.now())
            if self.status =='initialied':
                self.status = 'success'
            if self.pagenumber>1:
                self.pagenumber = self.pagenumber - 1   
            return True
        except:
            if self.status =='initialied':
                self.status = 'ERROR'
            return False

    def buildlink(self):
        self.baselink = 'https://www.%s.ir/%s/املاک/تهران'%(self.site,self.scrapetype)
        if self.site == 'ihome':
            sort_statement  = '?&sort=date_desc'
        if self.pagenumber > 1:
            self.currentlink = self.baselink + '/%i/'%(self.pagenumber) + sort_statement
        else:
            self.currentlink = self.baselink + sort_statement
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
            self.status = 'error in get Target Page Number'                
        
    def savePropertyFile (self,location,area,price,rooms,age,date):
        if date[0]==False:
            self.logger.debug('----def models.scrape.savePropertyFile: -----> verify date:FALSE')
            return([False , ''])
        if area < 30:
            self.logger.debug('----def models.scrape.savePropertyFile: -----> BAD AREA')
            return([False , ''])
        
        if price == [0,0] or rooms == 0:
            self.logger.debug('----def models.scrape.savePropertyFile: -----> BAD ROOM or PRICE')
            return([False , ''])
        
        if self.scrapetype == 'خرید-فروش':   #save data in database for BUY cases
            pm = price[0] / area
        elif self.scrapetype == 'رهن-اجاره': #save data in database for RENT cases
            total_price = price[1]+int((price[0]*100)/3)
            pm = total_price / area
            location = "%s - deposit:%i- rent:%i"%(location,price[1],price[0])

        this_file = PropertyFile(offertype = 1, location = location,area = area,\
                    price = pm, rooms = rooms,age = age, publishdate = make_aware(date[1]))
        this_file.save()
        self.logger.debug('----def models.scrape.savePropertyFile  -----> date saved:%s'%(date[1]))
        return([True , make_aware(date[1])])

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
            #TODO: most data returns 0! seprate new(0) and error91000) !   
            return 0

    def get_date(self,file):
        d = file.find('span',class_ = 'date left')
        try:
            d.span.extract()
            date_str = d.get_text(strip = True)   
        except:
            date_str = 'now'
        #self.logger.debug('----def models.scrape.get_date  -----> date:%s'%(date_str))
        return date_str
    
    def calculate_date(self,date_str):
        delta = self.extract_digit(date_str)
        validation = True
        if delta == 0:   # the publishdate is not valid - this file will not save in database
            validation = False
            self.logger.debug('----def models.scrape.calculate_date the publishdate is not valid')
            return [validation, datetime.now() - timedelta(days=365)]
        if re.search(r'دقیقه',date_str):  
            real_date = datetime.now() - timedelta(minutes=delta)
        elif re.search(r'ساعت',date_str):  
            real_date = datetime.now() - timedelta(hours=delta)
        elif re.search(r'روز',date_str):  
            real_date = datetime.now() - timedelta(days=delta)
        elif re.search(r'هفته',date_str):
            delta = 7 * delta  
            real_date = datetime.now() - timedelta(days=delta)
        elif re.search(r'بیش از',date_str):  # its over 6 months - this file will not save in database
            validation = False
            real_date = datetime.now() - timedelta(days=365)
        elif re.search(r'ماه',date_str):  
            real_date = datetime.now() - timedelta(days=delta*30)
        else:
            real_date = datetime.now() 
        return [validation,real_date]

    def extract_digit(self,my_str):
        digits = re.findall(r'\d+',my_str)
        try:
            return int(digits[0])
        except:
            self.logger.debug('----def models.scrape.extract_digit exception in extracting digit from %s'%my_str)
            return 0
        



