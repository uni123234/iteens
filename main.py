import logging, asyncio, sys

from handler.users_command import init_questions

from load import dp, bot, bot_db, db_users
import handler


@dp.startup()
async def on_startup(dispatcher):
    bot_db.open()
    db_users.connect(bot_db)
    db_users.create_default_tables()
    logging.info("Bot has runned")
    init_questions()

@dp.shutdown()
async def on_shutdown(dispatcher):
    bot_db.close()
    logging.info("Bot has stopped") 

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
