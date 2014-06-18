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
    fdate = datetime(2013,1,1) 
    tdate = datetime(2013,12,31)
    ndone = 0
    keys = {'maximale': 'tmax', 'minimale': 'tmin', 'Hauteur': 'rain', 'ensoleillement': 'sun'}

    def __init__(self):
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
        i =self.ndone
        prop = 100*i/float(self.ntodo)
        stdout.write("%s[%s] Done %i -- %s%f%%%s"%("\033[2K\r",
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            i,
            "\033[31m",
            prop,
            "\033[39m"))
        stdout.flush()

