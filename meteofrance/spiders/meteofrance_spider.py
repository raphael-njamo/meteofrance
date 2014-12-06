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
import os

class MeteofranceSpider(Spider):
    name = "meteofrance"
    allowed_domains = ["meteofrance.com"]

    base_url = "http://www.meteofrance.com/climat/meteo-date-passee?lieuId=%s&lieuType=%s&date=%s"
    ndone = 0
    tstart = datetime.now()
    keys = {'maximale': 'tmax', 'minimale': 'tmin', 'Hauteur': 'rain', 'ensoleillement': 'sun'}

    """
    Argument is a csv file of the format: place type, place id, date
    """
    def __init__(self,infile,outfile):
        self.outfile = os.path.abspath(outfile)
        with open(infile,"r") as c:
            csvr = csv.reader(c,delimiter=',')
            self.start_urls = [self.base_url%(r[1],r[0],r[2]) for r in csvr]
        self.ntodo = len(self.start_urls)
        stdout.write("Started scraping at %s. Going to scrape %i pages.\n"%(
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            self.ntodo))
        stdout.flush()

    def parse(self, response):
        # Meteofrance regularly return non-text responses
        try:
            sel = Selector(response)
        except:
            return response.request
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
                'mdate': response.url[-10:]})
            return MeteofranceItem(item)

    def log(self):
        i = float(self.ndone)
        prop = 100*i/self.ntodo
        now = datetime.now()
        selapsed = (now-self.tstart).seconds
        if selapsed>0:
            avsp = i/selapsed
            eta = now+timedelta(seconds=(self.ntodo-i)/avsp)
            stdout.write("%s[%s] Done %s -- %s -- Average speed: %s -- ETA: %s"%(
                "\033[2K\r",
                now.strftime("%d-%m-%Y %H:%M:%S"),
                i,
                "\033[33m%f%%\033[39m"%prop,
                "\033[35m%f\033[39m pages/s."%avsp,
                "\033[36m%s\033[39m"%eta.strftime("%d-%m-%Y %H:%M:%S")))
            stdout.flush()
