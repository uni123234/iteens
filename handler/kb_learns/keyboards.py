import random, json

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()

for index in range(1, 3):
    builder.button(text=f"Set {index}", callback_data=f"set:{index}")


keyboard = [ 
    [
        types.InlineKeyboardButton(text="Отримати нове слово", callback_data="learn_new_word")
    ]
] 
reply_markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)


file_path = 'handler/words.json'

with open(file_path, 'r', encoding='utf-8') as file:
    words_data = json.load(file)


def get_random_word():

    random_word = random.choice(words_data["words"])
    
    word = random_word["word"]
    translation = random_word["translation"]
    phrase = random_word["phrase"]

    inline_btn =[[ types.InlineKeyboardButton(text="Отримати нове слово", callback_data="learn_new_word")]]
    
    inline_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_btn)
    
    return [f"Слово: {word}\nПереклад: {translation}\nФраза: {phrase}", inline_kb]