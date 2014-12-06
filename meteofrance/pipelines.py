import codecs

class MySQLPipeline(object):

    def __init__(self):
        self.f = codecs.open("data.csv","w","utf-8")

    def process_item(self, item, spider):
        self.f.write("%s\n"%','.join(item.values()))
        return item

    def __del__(self):
        self.f.close()
