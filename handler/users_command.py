import json,random

from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from googletrans import Translator
from aiogram.types.inline_query import InlineQuery

from load import dp , bot, db_users
from db_learn.db_state import FSMRegister, FSMTranslate, FSMTest, FSMTestABC
from .kb_learns.keyboards import reply_markup
from .kb_learns.keyboard_test import reply_markups, backs, keyboard_t, reply_markupe, reply_markup_lvl, keyboard_test_a
from db_learn.db import DbUsers
from .kb_learns.keyboards import get_random_word

file_path = 'handler/words.json'

with open(file_path, 'r', encoding='utf-8') as file:
    words_data = json.load(file)

file_test = 'handler/test.json'

with open(file_test, 'r', encoding='utf-8') as file:
    test_data = json.load(file)


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


@dp.callback_query(F.data=="yes")
async def yess(call_back: types.CallbackQuery):
    await call_back.message.edit_text("Вибіріть рівень тест", reply_markup=reply_markup_lvl)


@dp.callback_query(F.data=="no")
async def yess(call_back: types.CallbackQuery):
    await call_back.message.delete()


@dp.callback_query(F.data=="a1")
async def a1_lvl(call_back: types.CallbackQuery, state: FSMContext):
    random_quest = random.choice(test_data['a1'])
    random_op = random_quest['options']
    random_qu = random_quest['question']
    correct = random_quest['correct_answer']
    kup = [*random_op]
    random.shuffle(kup) 

    await state.set_state(FSMTest.translation)
    await state.update_data(translation=correct)
    await state.set_state(FSMTestABC.tu)
    await state.update_data(tu='a1')
    await state.set_state(FSMTestABC.question)
    
    await call_back.message.answer(random_qu,reply_markup=keyboard_test_a(*kup))
    await state.clear()


# @dp.callback_query(F.data=="a2")
# async def a2_lvl(call_back: types.CallbackQuery, state: FSMContext):


# @dp.callback_query(F.data=="b1")
# async def b1_lvl(call_back: types.CallbackQuery, state: FSMContext):


# @dp.callback_query(F.data=="b2")
# async def b2_lvl(call_back: types.CallbackQuery, state: FSMContext):


# @dp.callback_query(F.data=="c1")
# async def c1_lvl(call_back: types.CallbackQuery, state: FSMContext):


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
    

@dp.callback_query()
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

