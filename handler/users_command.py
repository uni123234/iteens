import json,random

from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from googletrans import Translator

from load import dp , bot, db_users
from db_learn.db_state import FSMRegister, FSMTranslate, FSMTest
from .kb_learns.keyboards import reply_markup
from .kb_learns.keyboard_test import reply_markups
from db_learn.db import DbUsers
from .kb_learns.keyboards import get_random_word


file_path = 'handler/words.json'

with open(file_path, 'r', encoding='utf-8') as file:
    words_data = json.load(file)


@dp.message(Command("start"))
async def start(msg: types.Message, state: FSMContext):
    await msg.answer(f"Привіт, {msg.from_user.first_name}. Я допоможу тобі вивчити англійську мову☺")
    if db_users.check(msg.from_user.id) is None:
        await state.set_state(FSMRegister.first_name)
        await msg.answer("📥Для початку вам потрібно зареєструватися📥")
        await msg.answer("Введіть своє ім'я🖊️")
        

@dp.message(FSMRegister.first_name)
async def start_name(msg: types.Message, state: FSMContext):
    await state.update_data(first_name=msg.text)
    await state.set_state(FSMRegister.last_name)
    await msg.answer("📥Введіть своє прізвище📥")


@dp.message(FSMRegister.last_name)
async def start_last_name(msg: types.Message, state: FSMContext):
    # Monkey D. Luffy
    await state.update_data(last_name=msg.text)
    await state.set_state(FSMRegister.lng_lvl)
    await msg.answer("📥Введіть ваш рівень англійської📥")


@dp.message(FSMRegister.lng_lvl)
async def start_lng_lvl(msg: types.Message, state: FSMContext,):
    await state.update_data(lng_lvl=msg.text)
    get_info = await state.get_data()
    ints=DbUsers()

    ints.insert_user(
        username=msg.from_user.username,
        first_name=get_info.get("first_name"),
        last_name=get_info.get("last_name"),
        lng_lvl=get_info.get("lng_lvl"),
        telegram_id=msg.from_user.id, 
        progress=0
    )

    await msg.answer("📜Ви успішно зареєструвалися!📜")
    await state.clear()


@dp.message(Command("test"))
async def tests(msg: types.Message):
    if db_users.check(msg.from_user.id) is None:
        await msg.answer("Зарегіструйтеся будьласка через команду /start")
    else:
        text="📚Виберіть що тест📚"
        await msg.answer(text, reply_markup=reply_markups)

    
@dp.callback_query(F.data=="tests_one_word")
async def tests_one_word(call_back: types.CallbackQuery, state: FSMContext):
    random_word = random.choice(words_data["words"])
    word = random_word["word"]
    translation = random_word["translation"]
    await state.set_state(FSMTest.translation)
    await state.update_data(translation=word)
    await call_back.message.answer("📜Тестуваня буде в виді \nбот вам буде відправляти слова на укр\n а ви маєте відправити на Англ📜")
    await call_back.message.answer(translation)


@dp.callback_query(F.data=="tests_one_phrase")
async def tests_phrase(call_back: types.CallbackQuery, state: FSMContext):
    random_phrase = random.choice(words_data["words"])
    phrase = random_phrase["phrase"]
    translation = random_phrase["translation_phrase"]
    await state.set_state(FSMTest.translation)
    await state.update_data(translation=phrase)
    await call_back.message.answer("📜Тестуваня буде в виді \n вам буде відправлятися текст \n а ви його маєте перевести📜")
    await call_back.message.answer(translation)
    

@dp.message(FSMTest.translation)
async def transt_random(msg: types.Message, state: FSMContext):
    tests = await state.get_data()
    rty = tests.get('translation')
    if rty == msg.text.lower():
        await msg.answer('у вас +1 бал до прогресу🎓 все правильно🎓')
        say = db_users.get_progress(msg.from_user.id)
        db_users.update_user(msg.from_user.id, say + 1)
    else:
        await msg.answer("❌Ви відповіли не правильно❌")
        await msg.answer(f"Правильна відповідь {rty} 📚")
    await state.clear()


@dp.message(FSMTest.phrase)
async def transt_random(msg: types.Message, state: FSMContext):
    tests = await state.get_data()
    rty = tests.get('translation_phrase')
    if rty == msg.text.lower():
        await msg.answer('у вас +1 бал до прогресу🎓 все правильно🎓')
        say = db_users.get_progress(msg.from_user.id)
        db_users.update_user(msg.from_user.id, say + 1)
    else:
        await msg.answer("❌Ви відповіли не правильно❌")
        await msg.answer(f"Правильна відповідь {rty} 📚")
    await state.clear()


@dp.message(Command("learn"))
async def learn_words_and_synatx_word(msg: types.Message):
    if db_users.check(msg.from_user.id) is None:
        await msg.answer("Зарегіструйтеся будьласка через команду /start")
    else:
        text="📚Виберіть що хочете вивчити📚"
        say = db_users.get_progress(msg.from_user.id)

        db_users.update_user(msg.from_user.id, say + 0)
        await msg.answer(text, reply_markup=reply_markup)


@dp.message(Command("myprogress"))
async def progress_learn(msg: types.Message):
    if db_users.check(msg.from_user.id) is None:
        await msg.answer("Зарегіструйтеся будьласка через команду /start")
    else:
        say = db_users.get_progress(msg.from_user.id)
        await msg.answer("Ваш рівень англійського в балах📚 " + str(say) + " непогано)")


@dp.callback_query(F.data=="learn_new_word")
async def randoms_word(call_back: types.CallbackQuery ):
    mat = get_random_word()
    say = db_users.get_progress(call_back.from_user.id)
    db_users.update_user(call_back.from_user.id, say + 0)
    await call_back.message.edit_text(mat[0],reply_markup=mat[1])


@dp.message(Command("howdoisay"))
async def translaters(msg: types.Message, state: FSMContext) -> None:
    if db_users.check(msg.from_user.id) is None:
        await msg.answer("Зарегіструйтеся будьласка через команду /start")
    else:
        await state.set_state(FSMTranslate.text)
        await msg.answer("Введіть текст, який хочете переслакти україньською📲 ")


@dp.message(FSMTranslate.text)
async def trans(msg: types.Message, state:FSMContext):
    text = msg.text
    translator = Translator(service_urls=['translate.googleapis.com'])
    tr = translator.translate(text, dest='en')
    await msg.answer(tr.text)
    await state.clear()


@dp.message(Command("info"))
async def info_command(msg: types.Message):
    if db_users.check(msg.from_user.id) is None:
        await msg.answer("Зарегіструйтеся будьласка через команду /start")
    else:
        text=""" - Що може цей бот?🌆
    - Визначити твій рівень англійської🌇
    - Допомогти прокачати свої знання🎆
    - Давати рекомендації щодо вивчення нових слів та правил🎇
    - Давати завдання🌠
    - Допомогти тобі провести час із користю🛠 """
        await msg.answer(text)

