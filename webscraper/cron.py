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
            last_property_time = PropertyFile.objects.order_by('-publishdate')[0].publishdate
            first_property = PropertyFile.objects.order_by('publishdate')[0].publishdate
    
            logger.debug("----AutoCollectData, the last saved property is published on  ----->  %s"%last_property_time)
            logger.debug("----AutoCollectData, the first last property is published on  ----->  %s"%first_property)

            scrapeIhomeBuy = Scrape(scrapetype= 'خرید-فروش',last_update_time=last_property_time)
            if scrapeIhomeBuy.startscraping_update():
                scrapeIhomeBuy.save()
        except: 
            if  not PropertyFile.objects.all(): #property database is  empty
                scrapeIhomeBuy = Scrape(scrapetype= 'خرید-فروش',last_update_time=make_aware(datetime.now() - timedelta(days=60)))
                if scrapeIhomeBuy.startscraping_update():
                    scrapeIhomeBuy.save() 
                logger.debug('----AutoCollectData ----->  Database was empty! Data published in the last month was scraped successfully!')
            else:
                logger.debug('----AutoCollectData ----->  There was an unknown error in process of collecting data!!')
