import logging
from datetime import datetime,timedelta
from .models import Scrape, PropertyFile
from django.utils.timezone import make_aware
from django_cron import CronJobBase, Schedule

logger = logging.getLogger(__name__)
        
#class FixOffertype(CronJobBase):
#    RUN_AT_TIMES = ['4:02']
#   schedule = Schedule(run_at_times=RUN_AT_TIMES)
    
#    code = 'webscraper.FixOffertype'    # a unique code

#    def do(self):
#        buy = PropertyFile.objects.filter(offertype ='خرید-فروش')
#        buy.update(offertype=1)
#        logger.debug("----FixOffertype ----->  buy  %i"%buy.count())
#        rent = PropertyFile.objects.filter(offertype ='رهن-اجاره')
#        rent.update(offertype=2)
#        logger.debug("----FixOffertype ----->  rent %i"%rent.count())


class AutoCleanDB(CronJobBase):
    #RUN_EVERY_MINS = 120 # every 2 hours
    #schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    #TODO: extra data (more that 150 for each  location will be deleted)
    #TODO: if last update was not successfull try again some minutes later
    #TODO: consider that for each location there should be at least 50 records left

    RUN_AT_TIMES = ['4:02']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    
    code = 'webscraper.AutoCleanDB'    # a unique code

    def do(self):
        logger.debug("----AutoCleanDB ----->  is running")
        old_files = PropertyFile.objects.all()
        old_files.delete()
        
        # stage 1: delete old data
        logger.debug("----AutoCleanDB ----->   (stage 1):")
        treshhold = datetime.now() - timedelta(days=90)
        old_files = PropertyFile.objects.filter(publishdate__lt=make_aware(treshhold))
        old_files.delete()
        logger.debug("----AutoCleanDB ----->  (stage 1): %i files deleted."%old_files.count())
        
        # stage 2: delete redundant data
        logger.debug("----AutoCleanDB ----->   (stage 2):")
        count = 0
        for row in PropertyFile.objects.all():
            r= PropertyFile.objects.filter(offertype = row.offertype,location = row.location,area = row.area,\
                price1 = row.price1, price2 = row.price2, rooms = row.rooms, age = row.age, propertytype = row.propertytype).count()
            if r > 1:
                logger.debug("----AutoCleanDB ----->  (stage 2):%i CONFLICTS---- offertype:%s location:%s area:%i age:%i Deleted!!!"\
                    %(r, row.offertype,row.location,row.area,row.age))
                row.delete()
                count += 1
        logger.debug("----AutoCleanDB ----->  (stage 2): %i files deleted."%count)


class AutoCollectData(CronJobBase):
    #RUN_EVERY_MINS = 120 # every 2 hours
    #schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    RUN_AT_TIMES = ['02:02', '12:30', '18:15', '23:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    
    code = 'webscraper.AutoCollectData'    # a unique code

    def do(self):
        logger.debug("----AutoCollectData ----->  is running")
        this_propertytype = ['RES','COM','IND']
        this_offertype = [ (1,'خرید-فروش','BUY'),(2,'رهن-اجاره','RENT')]
        
        for i in this_offertype:
            for j in this_propertytype:
                logger.debug("----AutoCollectData -----> scraping for %s in %s  is running"%(i[2],j))
                try:    #property database is not empty
                    last_buy_property_time = PropertyFile.objects.filter(offertype = i[0],propertytype = j)\
                        .order_by('-publishdate')[0].publishdate
                    scrapeIhomeBuy = Scrape(scrapetype= i[1],last_update_time=last_buy_property_time,propertytype=j)
                    if scrapeIhomeBuy.startscraping_update():
                        scrapeIhomeBuy.save()
                        logger.debug('----AutoCollectData ----->I saved information about %s in %s in database!'%(i[2],j))
                    else: 
                        scrapeIhomeBuy.save() 
                        logger.debug('----AutoCollectData ----->%s in %s -- ERROR in startscraping_update!'%(i[2],j)) 
                except: 
                    if  not PropertyFile.objects.filter(offertype = i[0],propertytype = j): #property database is  empty
                        scrapeIhomeBuy = Scrape(scrapetype= i[1] ,propertytype = j,\
                            last_update_time=make_aware(datetime.now() - timedelta(days=60)))
                        if scrapeIhomeBuy.startscraping_update():
                            scrapeIhomeBuy.save() 
                            logger.debug('----AutoCollectData ----->There was no %s in %s files saved in DB!\
                                Data published in the last month was scraped successfully!'%(i[2],j))
                        else:
                            scrapeIhomeBuy.save()
                            logger.debug('----AutoCollectData -----> There was no %s in %s files saved in DB!\
                                 ERROR in startscraping_update!'%(i[2],j))
                    else:
                        logger.debug('----AutoCollectData ----->There was an error in process of collecting  %s in %s data!'%(i[2],j))
            
        logger.debug('----AutoCollectData -----> DONE')    
        
             #  logger.debug("----AutoCollectData ----->  is running")
          #  try:
            #    last_rent_property_time = PropertyFile.objects.filter(offertype = 2).order_by('-publishdate')[0].publishdate
            #    scrapeIhomeRent = Scrape(scrapetype= 'رهن-اجاره',last_update_time=last_rent_property_time)
            #    if scrapeIhomeRent.startscraping_update():
            #        scrapeIhomeRent.save()
             #       logger.debug('----AutoCollectData ----->I saved information about offertype = Rent in database!')
              #  else: 
               #     scrapeIhomeBuy.save() 
                #    logger.debug('----AutoCollectData ----->ERROR in startscraping_update!')
            #except: 
             #   if  not PropertyFile.objects.filter(offertype = 2): #property database is  empty
              #      scrapeIhomeRent = Scrape(scrapetype= 'رهن-اجاره',last_update_time=make_aware(datetime.now() - timedelta(days=60)))
               #     if scrapeIhomeRent.startscraping_update():
                #        scrapeIhomeRent.save() 
                 #       logger.debug('----AutoCollectData ----->There was no RENT files saved in DB! Data published in the last month was scraped successfully!')
                  #  else: 
                   #     scrapeIhomeBuy.save() 
                    #    logger.debug('----AutoCollectData ----->There was no RENT files saved in DB! ERROR in startscraping_update!')
            #    else:
             #       logger.debug('----AutoCollectData ----->There was an error in process of collecting  RENT data!')
           
    