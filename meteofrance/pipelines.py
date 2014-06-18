import MySQLdb
import os

class MySQLPipeline(object):
    
    MYSQL_DB_USERNAME = os.getenv('OPENSHIFT_MYSQL_DB_USERNAME','root') 
    MYSQL_DB_PASSWORD = os.getenv('OPENSHIFT_MYSQL_DB_PASSWORD','root')
    MYSQL_DB_SOCKET = os.getenv('OPENSHIFT_MYSQL_DB_SOCKET','/Applications/MAMP/tmp/mysql/mysql.sock')
    MYSQL_DB_DATABASE = 'weather'

    def __init__(self):
        self.db=MySQLdb.connect(user=self.MYSQL_DB_USERNAME,
                passwd=self.MYSQL_DB_PASSWORD,
                db=self.MYSQL_DB_DATABASE,
                unix_socket=self.MYSQL_DB_SOCKET)
        self.c=self.db.cursor()


    def process_item(self, item, spider):
        base_query = "INSERT IGNORE INTO %s (%s) VALUES (%s)"
        keys = item.keys()
        cols = ','.join(keys)
        vals = ','.join(['%%(%s)s'%k for k in keys])
        query = base_query%(item.table,cols,vals)
        self.c.execute(query,dict(item))
        self.db.commit()
        return item
