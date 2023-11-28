import load
from db_learn.db_a import DefaultInterface


class DbUsers(DefaultInterface):
    def create_default_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(32) NOT NULL,
                first_name VARCHAR(256),
                last_name VARCHAR(256),
                lng_lvl VARCHAR(2),
                telegram_id INTEGER,
                progress INTEGER 
            );       
        """)
        return self.conn.commit()


    def insert_user(self,lng_lvl: str, username: str, first_name: str = None, last_name: str = None, telegram_id: int = None, progress: int = 0):
        self.connect(load.bot_db)
        self.cursor.execute("""
            INSERT INTO users (username, first_name, last_name, lng_lvl, telegram_id, progress)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, first_name, last_name, lng_lvl, telegram_id, progress))

        return self.conn.commit()
    

    def update_user(self, telegram_id: int, progress: int):
        self.connect(load.bot_db)
        self.cursor.execute("""
            UPDATE users 
            SET progress = ?
            WHERE telegram_id = ?
        """, (progress, telegram_id))

        return self.conn.commit()


    def get_progress(self, telegram_id: int):
        self.connect(load.bot_db)
        self.cursor.execute(f"""
            SELECT progress
            FROM users
            WHERE telegram_id = ?
        """, (telegram_id, )) 

        return self.cursor.fetchone() [0]
    

    def check(self, telegram_id: int):
        self.connect(load.bot_db)
        self.cursor.execute('SELECT telegram_id FROM users WHERE telegram_id= ?', (telegram_id,))

        return self.cursor.fetchone()
    

    def update_lvl(self, telegram_id: int, lng_lvl: str):
        self.connect(load.bot_db)
        self.cursor.execute("""
            UPDATE users 
            SET lng_lvl = ?
            WHERE telegram_id = ?
        """, (lng_lvl, telegram_id))

        return self.conn.commit()
    

    def get_lng_lvl_by_telegram_id(self, telegram_id: int):
        self.connect(load.bot_db)
        self.cursor.execute("SELECT lng_lvl FROM users WHERE telegram_id=?", (telegram_id,))
        result = self.cursor.fetchone()
        if result:
            lng_lvl = result[0]
            return lng_lvl
        else:
            return None

