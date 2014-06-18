from scrapy.item import Item, Field

class MeteofranceItem(Item):
    table = 'meteofrance'

    sid = Field()
    mdate = Field()
    tmin = Field()
    tmax = Field()
    sun = Field()
    rain = Field()
