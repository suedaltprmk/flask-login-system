import sqlite3

class SqlUtilities:
    def __init__(self, db_path, table_sql):
        self.db_path = db_path
        self.db = sqlite3.connect(db_path)
        self.im = self.db.cursor()
        self.im.execute(table_sql)

    def disconnect(self):
        self.im.close()
        self.db.close()

    def reconnect(self):
        self.db = sqlite3.connect(self.db_path)
        self.im = self.db.cursor()

