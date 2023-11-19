import sqlite3

class BotDb:
    def __init__(self, db_file_name: str) -> None:
        self.db_file_name = db_file_name

    def open(self):
        self.conn = sqlite3.connect(self.db_file_name)
        self.cursor = self.conn.cursor()
    
    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close

class DefaultInterface:
    def connect(self, db_base: BotDb):
        self.conn = db_base.conn
        self.cursor = db_base.cursor