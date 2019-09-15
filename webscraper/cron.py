import logging
from datetime import datetime,timedelta
from .models import Scrape, PropertyFile
from django.utils.timezone import make_aware
from django_cron import CronJobBase, Schedule

logger = logging.getLogger(__name__)

class AutoCollectData(CronJobBase):
    #RUN_EVERY_MINS = 120 # every 2 hours
    #schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    RUN_AT_TIMES = ['02:02', '12:30', '18:15', '23:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    
    code = 'webscraper.AutoCollectData'    # a unique code

    def do(self):
        logger.debug("----AutoCollectData ----->  is running")
        try:    #property database is not empty
            last_buy_property_time = PropertyFile.objects.filter(offertype ='خرید-فروش').order_by('-publishdate')[0].publishdate
            scrapeIhomeBuy = Scrape(scrapetype= 'خرید-فروش',last_update_time=last_buy_property_time)
            if scrapeIhomeBuy.startscraping_update():
                scrapeIhomeBuy.save()
                logger.debug('----AutoCollectData ----->I saved information about offertype = Buy in database!')
            else: 
                scrapeIhomeBuy.save() 
                logger.debug('----AutoCollectData ----->ERROR in startscraping_update!') 
        except: 
            if  not PropertyFile.objects.filter(offertype ='خرید-فروش'): #property database is  empty
                scrapeIhomeBuy = Scrape(scrapetype= 'خرید-فروش',last_update_time=make_aware(datetime.now() - timedelta(days=60)))
                if scrapeIhomeBuy.startscraping_update():
                    scrapeIhomeBuy.save() 
                    logger.debug('----AutoCollectData ----->There was no BUY files saved in DB! Data published in the\
                         last month was scraped successfully!')
                else:
                    scrapeIhomeBuy.save()
                    logger.debug('----AutoCollectData -----> There was no BUY files saved in DB! ERROR in startscraping_update!')
            else:
                logger.debug('----AutoCollectData ----->There was an error in process of collecting  BUY data!')
    
        logger.debug("----AutoCollectData ----->  is running")
        try:
            last_rent_property_time = PropertyFile.objects.filter(offertype ='رهن-اجاره').order_by('-publishdate')[0].publishdate
            scrapeIhomeRent = Scrape(scrapetype= 'رهن-اجاره',last_update_time=last_rent_property_time)
            if scrapeIhomeRent.startscraping_update():
                scrapeIhomeRent.save()
                logger.debug('----AutoCollectData ----->I saved information about offertype = Rent in database!')
            else: 
                scrapeIhomeBuy.save() 
                logger.debug('----AutoCollectData ----->ERROR in startscraping_update!')
        except: 
            if  not PropertyFile.objects.filter(offertype ='رهن-اجاره'): #property database is  empty
                scrapeIhomeRent = Scrape(scrapetype= 'رهن-اجاره',last_update_time=make_aware(datetime.now() - timedelta(days=60)))
                if scrapeIhomeRent.startscraping_update():
                    scrapeIhomeRent.save() 
                    logger.debug('----AutoCollectData ----->There was no RENT files saved in DB! Data published in the last month was scraped successfully!')
                else: 
                    scrapeIhomeBuy.save() 
                    logger.debug('----AutoCollectData ----->There was no RENT files saved in DB! ERROR in startscraping_update!')
            else:
                logger.debug('----AutoCollectData ----->There was an error in process of collecting  RENT data!')
        logger.debug('----AutoCollectData -----> %s'%response)
    