"""
This module handles user commands for the English learning Telegram bot.

It includes functions for registration, tests, translation, and navigation.
"""

import random
from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from googletrans import Translator

from ..load import dp
from ..db_learn.fms_states import FSMRegister, FSMTranslate, FSMTest, FSMABCTest
from .kb_learns import (
    reply_markups,
    backs,
    keyboard_t,
    reply_markupe,
    dynamic_reply_db,
)
from ..config import WORDS, QUS, db_users


@dp.message(Command("start"))
async def start(msg: types.Message, state: FSMContext):
    """Start command handler. Greets the user and starts registration if necessary."""
    await msg.answer(
        f"Привіт, {msg.from_user.first_name}. Я допоможу тобі вивчити англійську мову☺"
    )

    if db_users.check_user(msg.from_user.id) is None:
        await state.set_state(FSMRegister.first_name)
        await msg.answer("📥Для початку вам потрібно зареєструватися📥")
        await msg.answer("Введіть своє ім'я🖊️")


@dp.message(FSMRegister.first_name)
async def start_name(msg: types.Message, state: FSMContext):
    """Handles user's first name during registration."""
    await state.update_data(first_name=msg.text)
    await state.set_state(FSMRegister.last_name)
    await msg.answer("📥Введіть своє прізвище📥")


@dp.message(FSMRegister.last_name)
async def start_last_name(msg: types.Message, state: FSMContext):
    """Handles user's last name during registration."""
    await state.update_data(last_name=msg.text)
    await state.set_state(FSMRegister.lng_lvl)
    await msg.answer("📥Введіть ваш рівень англійської📥")


@dp.message(FSMRegister.lng_lvl)
async def start_lng_lvl(msg: types.Message, state: FSMContext):
    """Handles user's language level during registration."""
    await state.update_data(lng_lvl=msg.text)
    user_data = await state.get_data()

    db_users.insert_user(
        username=msg.from_user.username,
        first_name=user_data.get("first_name"),
        last_name=user_data.get("last_name"),
        lng_lvl=user_data.get("lng_lvl"),
        telegram_id=msg.from_user.id,
        progress=0,
    )

    await msg.answer("📜Ви успішно зареєструвалися!📜")
    await msg.answer("📜Хочете пройти тест?📜", reply_markup=reply_markupe)
    await state.clear()


def question_generator(prev_number, curr_number, state_name, next_state):
    """Generates a callback query handler for a question."""

    @dp.callback_query(state_name)
    async def question(call_back: types.CallbackQuery, state: FSMContext):
        state_data = await state.get_data()
        if call_back.data == QUS[prev_number]["correct_answer"]:
            await state.update_data(
                score=state_data.get("score", 0) + QUS[prev_number]["point"]
            )
        await call_back.answer("Відповідь зарахована")
        await call_back.message.edit_text(
            f'{curr_number} Питання: \n{QUS[curr_number]["questions"]}',
            reply_markup=dynamic_reply_db(QUS[curr_number]["answers"]),
        )
        await state.set_state(next_state)


def init_questions():
    """Initializes the question handlers for the test."""
    for i in range(1, 25):
        question_generator(i, i + 1, FSMABCTest.q2 + i - 1, FSMABCTest.q2 + i)
    question_generator(25, 26, FSMABCTest.q25, FSMABCTest.final_q)

    @dp.callback_query(FSMTest.translation)
    async def test_answer(call_back: types.CallbackQuery, state: FSMContext):
        """Handles the answer for the translation test."""
        state_data = await state.get_data()
        translation = state_data.get("translation")
        if translation.lower() == call_back.data.lower():
            await call_back.message.edit_text(
                "у вас +1 бал до прогресу🎓 все правильно🎓",
                reply_markup=backs,
            )
            progress = db_users.get_progress(call_back.from_user.id)
            db_users.update_user(call_back.from_user.id, progress + 1)
        else:
            await call_back.message.edit_text("❌Ви відповіли не правильно❌")
            await call_back.message.answer(
                f"Правильна відповідь {translation} 📚",
                reply_markup=backs,
            )
        await state.clear()


@dp.callback_query(FSMABCTest.final_q)
async def final_test(call_back: types.CallbackQuery, state: FSMContext):
    """Handles the final test results and updates user's language level."""
    await call_back.message.delete()
    state_data = await state.get_data()
    score = state_data.get("score", 0)

    if score == 0:
        english_level = "A0"
    elif score > 60:
        english_level = "C1"
    elif score > 20:
        english_level = "B2"
    elif score > 10:
        english_level = "B1"
    elif score > 0:
        english_level = "A2"

    await call_back.message.answer(
        f"Тест закінчено! Твій рівень {english_level}\n"
        f"Твій результат - {score}/100",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await db_users.update_language_level(
        telegram_id=call_back.from_user.id, lng_lvl=english_level
    )
    await state.clear()


@dp.callback_query(F.data == "a1")
async def start_test(call_back: types.CallbackQuery, state: FSMContext):
    """Starts the test for level A1."""
    if db_users.check_user(call_back.from_user.id) is not None:
        await state.update_data(score=0)
        await call_back.message.answer("1 Питання:")
        await call_back.message.answer(
            QUS[1]["questions"],
            reply_markup=dynamic_reply_db(QUS[1]["answers"]),
        )
        await state.set_state(FSMABCTest.q2)
    else:
        await call_back.message.answer("Зареєструйся!")


@dp.callback_query(F.data == "back_to_tests")
async def back_to_tests(call_back: types.CallbackQuery):
    """Returns the user to the test selection menu."""
    text = "📚Виберіть що тест📚"
    await call_back.message.edit_text(text, reply_markup=reply_markups)


@dp.message(Command("test"))
async def start_tests(msg: types.Message):
    """Starts the test selection process."""
    if db_users.check_user(msg.from_user.id) is None:
        await msg.answer("Зарегіструйтеся будьласка через команду /start")
    else:
        text = "📚Виберіть що тест📚"
        await msg.answer(text, reply_markup=reply_markups)


@dp.callback_query(F.data == "tests_one_word")
async def test_one_word(call_back: types.CallbackQuery, state: FSMContext):
    """Handles the 'one word' test."""
    random_word = random.choice(WORDS["words"])
    word = random_word["word"]
    translation = random_word["translation"]
    options = [random.choice(WORDS["words"])["word"] for _ in range(3)]
    options.append(word)
    random.shuffle(options)
    kb = keyboard_t(*options)
    await call_back.message.edit_text(
        text="📜Тестуваня буде в виді вибору правильного слова, "
        "до перекладу📜\n📜Для початку надішліть рівень складності📜",
        reply_markup=kb,
    )
    await state.update_data(translation=translation)
    await state.set_state(FSMTest.translation)


@dp.message(FSMTest.translation)
async def test_translation(msg: types.Message, state: FSMContext):
    """Handles translation test input from the user."""
    state_data = await state.get_data()
    translation = state_data.get("translation")
    if translation.lower() == msg.text.lower():
        await msg.answer("у вас +1 бал до прогресу🎓 все правильно🎓")
        progress = db_users.get_progress(msg.from_user.id)
        db_users.update_user(msg.from_user.id, progress + 1)
    else:
        await msg.answer("❌Ви відповіли не правильно❌")
        await msg.answer(f"Правильна відповідь {translation} 📚")
    await state.clear()


@dp.message(Command("help"))
async def help_cmd(msg: types.Message):
    """Provides help information."""
    await msg.answer(
        "/start - розпочати\n/test - почати тест\n/help - допомога\n\n"
        "Цей бот допоможе вам вивчити англійську мову!"
    )


@dp.callback_query(F.data == "back")
async def go_back(call_back: types.CallbackQuery):
    """Navigates back to the main menu."""
    await call_back.message.delete()
    await call_back.message.answer(
        "Ви повернулися до головного меню📜", reply_markup=backs
    )


@dp.message(Command("translate"))
async def translate_command(msg: types.Message, state: FSMContext):
    """Initiates the translation process."""
    await msg.answer("Введіть текст, який ви хочете перекласти:")
    await state.set_state(FSMTranslate.text)


@dp.message(FSMTranslate.text)
async def translate_text(msg: types.Message, state: FSMContext):
    """Handles text translation and sends the result."""
    translator = Translator()
    try:
        translation = translator.translate(msg.text, dest="en")
        await msg.answer(translation.text)
    except ValueError as e:
        await msg.answer("Сталася помилка під час перекладу. Спробуйте ще раз.")
        print(f"Translation error: {e}")
    except RuntimeError as e:
        await msg.answer("Сталася несподівана помилка. Спробуйте ще раз пізніше.")
        print(f"Unexpected runtime error: {e}")
    finally:
        await state.finish()
