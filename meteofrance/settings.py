LOG_LEVEL = 'WARNING'

BOT_NAME = 'meteofrance'

SPIDER_MODULES = ['meteofrance.spiders']
NEWSPIDER_MODULE = 'meteofrance.spiders'

DUPEFILTER_CLASS = 'scrapy.dupefilter.BaseDupeFilter'

ITEM_PIPELINES = {'meteofrance.pipelines.MySQLPipeline': 1000}

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'

CONCURRENT_REQUESTS_PER_DOMAIN = 64

WEBSERVICE_ENABLED = False
TELNETCONSOLE_ENABLED = False

DOWNLOADER_MIDDLEWARES = {'meteofrance.middlewares.ProxyMiddleware': 1000}
