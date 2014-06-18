from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from datetime import datetime, timedelta
from meteofrance.spiders.meteofrance_spider import MeteofranceSpider
import sys

class Manager(object):

    settings = get_project_settings()
    fdate = datetime(2014,1,1) 
    tdate = datetime(2014,6,11)
    
    def __init__(self):
        self.dates = [d for d in self.dates()]
        self.ndates = len(self.dates)

    def dates(self):
        d = self.fdate
        while d<=self.tdate:
            yield d
            d=d+timedelta(1)

    def schedule_next(self):
        try:
            reactor.stop()
        except:
            pass
        if len(self.dates)>0:
            date = self.dates.pop()
            self.log()
            spider = MeteofranceSpider(date)
            crawler = Crawler(self.settings)
            crawler.signals.connect(self.schedule_next, signal=signals.spider_closed)
            crawler.configure()
            crawler.crawl(spider)
            crawler.start()
            log.start(log.WARNING)
            reactor.run()

    def log(self):
        prop = 100-100*len(self.dates)/float(self.ndates)
        sys.stdout.write('\rDone %f%%'%prop) 
        sys.stdout.flush()

if __name__=="__main__":
    m = Manager()
    m.schedule_next()
