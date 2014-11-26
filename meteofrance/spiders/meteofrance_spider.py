from scrapy.spider import Spider
from scrapy.http import Request, Response
from scrapy.selector import Selector
from meteofrance.items import MeteofranceItem
import re
from datetime import datetime, timedelta, date
import csv
import pkgutil
import itertools
from sys import stdout

class MeteofranceSpider(Spider):
    name = "meteofrance"
    allowed_domains = ["meteofrance.com"]

    base_url = "http://www.meteofrance.com/climat/meteo-date-passee?lieuId=%08d&lieuType=STATION_CLIM_FR&date=%02d-%02d-%04d"
    ndone = 0
    tstart = datetime.now()
    keys = {'maximale': 'tmax', 'minimale': 'tmin', 'Hauteur': 'rain', 'ensoleillement': 'sun'}

    def __init__(self,year):
        self.fdate = datetime(int(year),1,1) 
        self.tdate = datetime(int(year),12,31)
        s=pkgutil.get_data('meteofrance','meteofrance_stations.csv')
        csvr = csv.reader(s.split('\n'),delimiter=',')
        self.start_urls = [self.base_url%(int(r[0]),
            d.day,d.month,d.year) for r,d in itertools.product(csvr,self.dates())]
        self.ntodo = len(self.start_urls)
        stdout.write("Started scraping at %s. Going to scrape %i pages.\n"%(
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            self.ntodo))
        stdout.flush()

    def dates(self):
        d = self.fdate
        while d<=self.tdate:
            yield d
            d=d+timedelta(1)

    def parse(self, response):
        sel = Selector(response)
        data = sel.xpath("//div[@id='p_p_id_meteoDuPasse_WAR_mf3rpcportlet_']//li/text()").extract()
        self.ndone+=1
        self.log()
        if len(data)==0:
            return None
        else:
            item = {v:''.join(re.split('(\d+)',s)[1::2]) 
                for s in data for u,v in self.keys.iteritems() 
                if re.search(u,s)!=None}
            item.update({'sid':re.split('(\d+)',response.url)[1],
                'mdate': datetime.strptime(response.url[-10:],"%d-%m-%Y")})
            return MeteofranceItem(item)

    def log(self):
        i = float(self.ndone)
        prop = 100*i/self.ntodo
        now = datetime.now()
        avsp = i/(now-self.tstart).seconds
        eta = now+timedelta(seconds=(self.ntodo-i)/avsp)
        stdout.write("%s[%s] Done %s -- %s -- Average speed: %s -- ETA: %s"%(
            "\033[2K\r",
            now.strftime("%d-%m-%Y %H:%M:%S"),
            i,
            "\033[33m%f%%\033[39m"%prop,
            "\033[35m%f\033[39m pages/s."%avsp,
            "\033[36m%s\033[39m"%eta.strftime("%d-%m-%Y %H:%M:%S")))
        stdout.flush()
