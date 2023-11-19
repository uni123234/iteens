import logging

from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from googletrans import Translator

from load import dp
from db_learn.db_state import FSMRegister
from .kb_learns.keyboards import reply_markup, builder

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
    text="Виберіть що хочете вивчити"
    await msg.answer(text, reply_markup=reply_markup)


@dp.message(Command("howdoisay"))
async def translaters(msg: types.Message):
    cmd: Command = msg.command_handlers[0]
    args = cmd.args
    if len(args) == 0:
        await msg.reply('Enter a valid text!')



@dp.message(Command("info"))
async def info_command(msg: types.Message):
    text=""" - Що може цей бот?🌆
 - Визначити твій рівень англійської🌇
 - Допомогти прокачати свої знання🎆
 - Давати рекомендації щодо вивчення нових слів та правил🎇
 - Давати завдання🌠
 - Допомогти тобі провести час із користю🛠 """
    await msg.answer(text)

