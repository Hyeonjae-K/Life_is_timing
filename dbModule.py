import pymysql

with open('./info.txt', encoding='UTF-8') as f:
    host = f.readline().strip()
    user = f.readline().strip()
    password = f.readline().strip()
    db = f.readline().strip()
    charset = f.readline().strip()


class Database():
    def __init__(self):
        self.db = pymysql.connect(host=host,
                                  user=user,
                                  password=password,
                                  db=db,
                                  charset=charset)
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def commit(self):
        self.db.commit()