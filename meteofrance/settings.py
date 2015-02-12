LOG_LEVEL = 'WARNING'

BOT_NAME = 'meteofrance'

SPIDER_MODULES = ['meteofrance.spiders']
NEWSPIDER_MODULE = 'meteofrance.spiders'

DUPEFILTER_CLASS = 'scrapy.dupefilter.BaseDupeFilter'
#DOWNLOADER_MIDDLEWARES={'meteofrance.middlewares.ProxyMiddleware': 100}

FEED_FORMAT = 'csv'
FEED_URI = 'file://%(outfile)s'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'

CONCURRENT_REQUESTS= 32
CONCURRENT_REQUESTS_PER_DOMAIN = 32

WEBSERVICE_ENABLED = False
TELNETCONSOLE_ENABLED = False
