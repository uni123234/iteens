from environs import Env
from ..handler.utils import load_test_data, load_words_data
from ..handler.utils import load_questions

from ..load import bot_db
from ..db_learn import DbUsers

env = Env()
env.read_env()
db_users = DbUsers(bot_db)

BOT_TOKEN = env.str("BOT_TOKEN")
DB_FILE = env.str("DB_FILE")

WORDS = load_words_data("json/words.json")
TESTS = load_test_data("json/test.json")

QUS = load_questions(TESTS)
