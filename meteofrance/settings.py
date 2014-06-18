LOG_LEVEL = 'WARNING'

BOT_NAME = 'meteofrance'

SPIDER_MODULES = ['meteofrance.spiders']
NEWSPIDER_MODULE = 'meteofrance.spiders'

DUPEFILTER_CLASS = 'scrapy.dupefilter.BaseDupeFilter'

ITEM_PIPELINES = {'meteofrance.pipelines.MySQLPipeline': 1000}

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'

WEBSERVICE_ENABLED = False
WEBSERVICE_PORT = 8080
TELNETCONSOLE_ENABLED = False

EXTENSIONS = {
    'scrapy.contrib.corestats.CoreStats': 500,
    'scrapy.webservice.WebService': None,
    'scrapy.telnet.TelnetConsole': None,}
