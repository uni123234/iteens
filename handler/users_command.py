import logging

from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from googletrans import Translator

from load import dp
from db_learn.db_state import FSMRegister
from .kb_learns.keyboards import kb_learn, builder

translator = Translator()


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
async def start_lng_lvl(msg: types.Message, state: FSMContext):
    await state.update_data(lng_lvl=msg.text)


@dp.message(Command("learn"))
async def learn_words_and_synatx_word(msg: types.Message):
    await msg.answer("Some text here", reply_markup=builder.as_markup())


@dp.message(Command("howdoisay"))
async def translaters(msg: types.Message, state: FSMContext) -> None:
    if len(msg.get_args()) == 0:
        await msg.reply("Please provide text to translate. Usage: /howdoisay <text>")
        return

    text_to_translate = " ".join(msg.get_args())

    translated_text = translator.translate(text_to_translate, dest='en').text

    response_message = f'Translation: {translated_text}'
    await msg.reply(response_message)


@dp.message(Command("info"))
async def info_command(msg: types.Message):
    await msg.answer(""" - Що може цей бот?
 - Визначити твій рівень англійської
 - Допомогти прокачати свої знання
 - Давати рекомендації щодо вивчення нових слів та правил
 - Давати завдання
 - Допомогти тобі провести час із користю """)

