from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data import config_bot
from db_learn import BotDb, DbUsers

bot = Bot(token=config_bot.BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

bot_db = BotDb(config_bot.DB_FILE)
db_users = DbUsers()
