"""
This module initializes the bot, sets up event handling, and manages the bot's lifecycle.
"""

import logging
import asyncio
import sys

from handler.users_command import init_questions
from load import dp, bot, bot_db, db_users


@dp.startup()
async def on_startup():
    """
    Called when the bot starts up.
    """
    bot_db.open()
    db_users.connect(bot_db)
    db_users.setup()
    logging.info("Bot has run")
    init_questions()

@dp.shutdown()
async def on_shutdown():
    """
    Called when the bot shuts down.
    """
    bot_db.close()
    logging.info("Bot has stopped")

async def main():
    """
    Starts the bot's polling loop.
    """
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
