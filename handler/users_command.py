import json,random

from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from googletrans import Translator
from aiogram.types.inline_query import InlineQuery

from load import dp , bot, db_users
from db_learn.db_state import FSMRegister, FSMTranslate, FSMTest, FSMABCTest
from .kb_learns.keyboards import reply_markup
from .kb_learns.keyboard_test import reply_markups, backs, keyboard_t, reply_markupe, reply_markup_lvl, dynamic_reply_db
from db_learn.db import DbUsers
from .kb_learns.keyboards import get_random_word

file_path = 'handler/words.json'

with open(file_path, 'r', encoding='utf-8') as file:
    words_data = json.load(file)

file_test = 'handler/test.json'

with open(file_test, 'r', encoding='utf-8') as file:
    test_data = json.load(file)

num = 1
qus = dict()
for data in test_data['questions']:
    qus[num] = data
    num += 1


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
    await msg.answer("📜Хочете пройти тест?📜", reply_markup=reply_markupe)
    await state.clear()


def question_generator(prev_number, curr_number, state_name, next_state):
    @dp.callback_query(state_name)
    async def question(call_back: types.CallbackQuery, state: FSMContext):
        our_data = await state.get_data()
        if call_back.data == qus[prev_number]["correct_answer"]:
            await state.update_data(
                {
                    "score":our_data['score'] + qus[prev_number]["point"]
                }
                
            )
        await call_back.answer(f"Відповідь зарахована")
        await call_back.message.edit_text(f'{curr_number} Питання: \n {qus[curr_number]["questions"]}', reply_markup=dynamic_reply_db(qus[curr_number]["answers"]))
        await state.set_state(next_state)


def init_questions():
    question_generator(1, 2, FSMABCTest.q2, FSMABCTest.q3)
    question_generator(2, 3, FSMABCTest.q3, FSMABCTest.q4)
    question_generator(3, 4, FSMABCTest.q4, FSMABCTest.q5)
    question_generator(4, 5, FSMABCTest.q5, FSMABCTest.q6)
    question_generator(5, 6, FSMABCTest.q6, FSMABCTest.q7)
    question_generator(6, 7, FSMABCTest.q7, FSMABCTest.q8)
    question_generator(7, 8, FSMABCTest.q8, FSMABCTest.q9)
    question_generator(8, 9, FSMABCTest.q9, FSMABCTest.q10)
    question_generator(9, 10, FSMABCTest.q10, FSMABCTest.q11)
    question_generator(10, 11, FSMABCTest.q11, FSMABCTest.q12)
    question_generator(12, 13, FSMABCTest.q12, FSMABCTest.q13)
    question_generator(13, 14, FSMABCTest.q13, FSMABCTest.q14)
    question_generator(14, 15, FSMABCTest.q14, FSMABCTest.q15)
    question_generator(15, 16, FSMABCTest.q15, FSMABCTest.q16)
    question_generator(16, 17, FSMABCTest.q16, FSMABCTest.q17)
    question_generator(17, 18, FSMABCTest.q17, FSMABCTest.q18)
    question_generator(18, 19, FSMABCTest.q18, FSMABCTest.q19)
    question_generator(19, 20, FSMABCTest.q19, FSMABCTest.q20)
    question_generator(20, 21, FSMABCTest.q20, FSMABCTest.q21)
    question_generator(21, 22, FSMABCTest.q21, FSMABCTest.q22)
    question_generator(22, 23, FSMABCTest.q22, FSMABCTest.q23)
    question_generator(23, 24, FSMABCTest.q23, FSMABCTest.q24)
    question_generator(24, 25, FSMABCTest.q24, FSMABCTest.q25)
    question_generator(25, 26, FSMABCTest.q25, FSMABCTest.final_q)


    @dp.callback_query(FSMTest.translation)
    async def test_answer(call_back: types.CallbackQuery, state: FSMContext):
        tests = await state.get_data()
        rty = tests.get('translation')
        if rty.lower() == call_back.data.lower():
            await call_back.message.edit_text('у вас +1 бал до прогресу🎓 все правильно🎓', reply_markup=backs)
            say = db_users.get_progress(call_back.from_user.id)
            db_users.update_user(call_back.from_user.id, say + 1)
        else:
            await call_back.message.edit_text("❌Ви відповіли не правильно❌")
            await call_back.message.answer(f"Правильна відповідь {rty} 📚", reply_markup=backs)

        await state.clear()


@dp.callback_query(FSMABCTest.final_q)
async def my_test(call_back: types.CallbackQuery, state: FSMContext):
    await call_back.message.delete()
    our_data = await state.get_data()

    score = our_data['score']
    english_level = "A1"
    if score == 0:
        await call_back.message.answer("У тебе A0, біжи вчитись!")
    elif score > 10:
        english_level = "A2"
    elif 20>score > 10:
        english_level = "B1"
    elif 60>score > 10:
        english_level = "B2"
    elif 60>score > 100:
        english_level = "C1"

    await call_back.message.answer(f"Тест закінчено! Твій рівень {english_level}\nТвій результат - {score}/100", reply_markup=types.ReplyKeyboardRemove())
    await db_users.update_lvl(telegram_id=call_back.from_user.id, lng_lvl=english_level)
    await state.clear()


@dp.callback_query(F.data=="a1")
async def my_test(call_back: types.CallbackQuery, state: FSMContext):
    if db_users.check(call_back.from_user.id) is not None:
        await state.update_data(score=0)
        await call_back.message.answer(f"1 Питання:")
        await call_back.message.answer(qus[1]["question"], reply_markup=dynamic_reply_db(qus[1]["answers"]))
        await state.set_state(FSMABCTest.q2)
    else:
        await call_back.message.answer("Зареєструйся!")


@dp.callback_query(F.data=="yes")
async def yess(call_back: types.CallbackQuery):
    await call_back.message.edit_text("Вибіріть рівень тест", reply_markup=reply_markup_lvl)


@dp.callback_query(F.data=="no")
async def yess(call_back: types.CallbackQuery):
    await call_back.message.delete()


@dp.callback_query(F.data=="back_to_tests")
async def back(call_back: types.CallbackQuery):
        text="📚Виберіть що тест📚"
        await call_back.message.edit_text(text, reply_markup=reply_markups)


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
    kupa = []
    for words in range(3):
        kupa.append(random.choice(words_data["words"])['word'])
    else:
        kupa.append(word)
    random.shuffle(kupa)
    kb = keyboard_t(*kupa)
    await call_back.message.edit_text(text="📜Тестуваня буде в виді \nбот вам буде відправляти слова на укр\n а ви маєте відправити на Англ📜")
    await state.set_state(FSMTest.translation)
    await state.update_data(translation=word)
    await call_back.message.answer(translation, reply_markup=kb)


@dp.callback_query(F.data=="tests_one_phrase")
async def tests_phrase(call_back: types.CallbackQuery, state: FSMContext):
    random_phrase = random.choice(words_data["words"])
    phrase = random_phrase["phrase"]
    translation = random_phrase["translation_phrase"]
    kupa = []
    for words in range(3):
        kupa.append(random.choice(words_data["words"])['phrase'])
    else:
        kupa.append(phrase)
    random.shuffle(kupa)
    kb = keyboard_t(*kupa) 
    await call_back.message.edit_text(text="📜Тестуваня буде в виді \n вам буде відправлятися текст \n а ви його маєте перевести📜")
    await state.set_state(FSMTest.translation)
    await state.update_data(translation=phrase)
    await call_back.message.answer(translation, reply_markup=kb)
    

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
    