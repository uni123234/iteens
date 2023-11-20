from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from googletrans import Translator

from load import dp , bot
from db_learn.db_state import FSMRegister, FSMTranslate
from kb_learns.keyboards import reply_markup
from db_learn.db import DbUsers
from .kb_learns.keyboards import get_random_word


@dp.message(Command("start"))
async def start(msg: types.Message, state: FSMContext):
    await state.set_state(FSMRegister.first_name)
    await msg.answer(f"Привіт, {msg.from_user.first_name}. Я допоможу тобі вивчити англійську мову☺")
    await msg.answer("Для початку вам потрібно зареєструватися")
    await msg.answer("Введіть своє ім'я")


@dp.message(FSMRegister.first_name)
async def start_name(msg: types.Message, state: FSMContext):
    await state.update_data(first_name=msg.text)
    await state.set_state(FSMRegister.last_name)
    await msg.answer("Введіть своє прізвище")


@dp.message(FSMRegister.last_name)
async def start_last_name(msg: types.Message, state: FSMContext):
    # Monkey D. Luffy
    await state.update_data(last_name=msg.text)
    await state.set_state(FSMRegister.lng_lvl)
    await msg.answer("Введіть ваш рівень англійської")


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

    await msg.answer("Ви успішно зареєструвалися!")
    await state.clear()

@dp.message(Command("learn"))
async def learn_words_and_synatx_word(msg: types.Message):
    text="Виберіть що хочете вивчити"
    db = DbUsers()
    say = db.get_progress(msg.from_user.id)
    suma = int(say[0])+1
    db.update_user(msg.from_user.id, suma)
    await msg.answer(text, reply_markup=reply_markup)

@dp.message(Command("myprogress"))
async def progress_learn(msg: types.Message):
    db = DbUsers()
    say = db.get_progress(msg.from_user.id)
    await msg.answer(str(say[0]))


@dp.callback_query(F.data=="learn_new_word")
async def randoms_word(call_back: types.CallbackQuery ):
    mat = get_random_word()
    db = DbUsers()
    say = db.get_progress(call_back.from_user.id)
    suma = int(say[0])+1
    db.update_user(call_back.from_user.id, suma)
    await bot.delete_message(call_back.message.chat.id, call_back.message.message_id)
    await call_back.message.answer(mat[0],reply_markup=mat[1])


@dp.message(Command("howdoisay"))
async def translaters(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(FSMTranslate.text)
    await msg.answer("Введіть текст, який хочете переслакти англійською")


@dp.message(FSMTranslate.text)
async def trans(msg: types.Message, state:FSMContext):
    text = msg.text
    translator = Translator(service_urls=['translate.googleapis.com'])
    tr = translator.translate(text, dest='en')
    await msg.answer(tr.text)
    await state.clear()


@dp.message(Command("info"))
async def info_command(msg: types.Message):
    text=""" - Що може цей бот?🌆
 - Визначити твій рівень англійської🌇
 - Допомогти прокачати свої знання🎆
 - Давати рекомендації щодо вивчення нових слів та правил🎇
 - Давати завдання🌠
 - Допомогти тобі провести час із користю🛠 """
    await msg.answer(text)

