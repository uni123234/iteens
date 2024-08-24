"""
This module initializes the bot, sets up the dispatcher, and connects to the database.
"""

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import DB_FILE, BOT_TOKEN
from db_learn import BotDb, DbUsers

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

bot_db = BotDb(DB_FILE)
db_users = DbUsers(db_base="learn.db")
