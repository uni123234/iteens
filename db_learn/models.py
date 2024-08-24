from .db import BotDb
from .schema import create_default_tables


class DefaultInterface:
    """
    Provides methods to connect to a database.
    """

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, db_base: BotDb):
        """
        Connects to the database and sets the cursor.

        Args:
            db_base (BotDb): An instance of BotDb providing the connection and cursor.
        """
        self.conn = db_base.conn
        self.cursor = db_base.cursor


class DbUsers(DefaultInterface):
    """
    Provides methods for user-related database operations.
    """

    def __init__(self, db_base: BotDb):
        super().__init__()
        self.connect(db_base)
        self.setup()

    def setup(self):
        """
        Sets up the database schema.
        """
        create_default_tables(self.cursor, self.conn)

    def insert_user(
        self,
        lng_lvl: str,
        username: str,
        first_name: str = None,
        last_name: str = None,
        telegram_id: int = None,
        progress: int = 0,
    ):
        """
        Inserts a new user into the database.

        Args:
            lng_lvl (str): Language level of the user.
            username (str): Username of the user.
            first_name (str, optional): First name of the user.
            last_name (str, optional): Last name of the user.
            telegram_id (int, optional): Telegram ID of the user.
            progress (int, optional): Progress of the user. Defaults to 0.
        """
        self.cursor.execute(
            """
            INSERT INTO users (username, first_name, last_name, lng_lvl, telegram_id, progress)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (username, first_name, last_name, lng_lvl, telegram_id, progress),
        )
        self.conn.commit()

    def update_user(self, telegram_id: int, progress: int):
        """
        Updates the progress of a user.

        Args:
            telegram_id (int): Telegram ID of the user.
            progress (int): New progress value.
        """
        self.cursor.execute(
            """
            UPDATE users 
            SET progress = ?
            WHERE telegram_id = ?
        """,
            (progress, telegram_id),
        )
        self.conn.commit()

    def get_progress(self, telegram_id: int):
        """
        Retrieves the progress of a user.

        Args:
            telegram_id (int): Telegram ID of the user.

        Returns:
            int: The progress of the user.
        """
        self.cursor.execute(
            """
            SELECT progress
            FROM users
            WHERE telegram_id = ?
        """,
            (telegram_id,),
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def check_user(self, telegram_id: int):
        """
        Checks if a user exists in the database.

        Args:
            telegram_id (int): Telegram ID of the user.

        Returns:
            tuple: The result of the query.
        """
        self.cursor.execute(
            "SELECT telegram_id FROM users WHERE telegram_id = ?", (telegram_id,)
        )
        return self.cursor.fetchone()

    def update_language_level(self, telegram_id: int, lng_lvl: str):
        """
        Updates the language level of a user.

        Args:
            telegram_id (int): Telegram ID of the user.
            lng_lvl (str): New language level.
        """
        self.cursor.execute(
            """
            UPDATE users 
            SET lng_lvl = ?
            WHERE telegram_id = ?
        """,
            (lng_lvl, telegram_id),
        )
        self.conn.commit()

    def get_language_level(self, telegram_id: int):
        """
        Retrieves the language level of a user.

        Args:
            telegram_id (int): Telegram ID of the user.

        Returns:
            str: The language level of the user, or None if not found.
        """
        self.cursor.execute(
            "SELECT lng_lvl FROM users WHERE telegram_id = ?", (telegram_id,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None
