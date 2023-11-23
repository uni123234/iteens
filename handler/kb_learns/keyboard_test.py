from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()

for index in range(1, 3):
    builder.button(text=f"Set {index}", callback_data=f"set:{index}")

keyboard_test = [
    [
       types.InlineKeyboardButton(text="📜Тест по одному слову📜", callback_data="tests_one_word"), 
       types.InlineKeyboardButton(text="📜Тест на часи📜", callback_data="tests_one_phrase"),  
    ]
]
reply_markups = types.InlineKeyboardMarkup(inline_keyboard=keyboard_test)