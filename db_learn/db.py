"""
This module defines the BotDb class for managing database connections.

The BotDb class provides methods to:
- Open a connection to a SQLite database.
- Initialize a cursor for executing SQL commands.
- Close the database connection.
"""

import sqlite3

class BotDb:
    """
    Manages database connection and cursor.
    """

    def __init__(self, db_file_name: str) -> None:
        """
        Initializes the BotDb instance with the database file name.

        Args:
            db_file_name (str): The path to the SQLite database file.
        """
        self.db_file_name = db_file_name
        self.conn = None
        self.cursor = None

    def open(self):
        """
        Opens a connection to the database and initializes the cursor.
        """
        self.conn = sqlite3.connect(self.db_file_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()
