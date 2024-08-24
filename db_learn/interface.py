"""
This module defines the DefaultInterface class for managing database connections.

The DefaultInterface class provides a method to connect to a database and set up 
the connection and cursor attributes.
"""

from .db import BotDb


class DefaultInterface:
    """
    A base class for managing database connections.

    This class holds attributes for a database connection and cursor and provides
    a method to connect to a database using a BotDb instance.
    """

    def __init__(self):
        """
        Initializes the DefaultInterface instance with no connection or cursor.
        """
        self.conn = None
        self.cursor = None

    def connect(self, db_base: BotDb):
        """
        Connects to the given BotDb instance and sets up the connection and cursor.

        Args:
            db_base (BotDb): An instance of the BotDb class that provides the
            database connection and cursor.
        """
        self.conn = db_base.conn
        self.cursor = db_base.cursor
