"""
This module initializes the db_learn package.

It includes the following components:
- BotDb: A class for managing database connections.
- DbUsers: A class for performing user-related database operations.
"""

from .db import BotDb
from .models import DbUsers
from .schema import create_default_tables
