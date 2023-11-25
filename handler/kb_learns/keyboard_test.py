from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


keyboard_test = [
    [
       types.InlineKeyboardButton(text="📜Тест по одному слову📜", callback_data="tests_one_word"), 
       types.InlineKeyboardButton(text="📜Тест на часи📜", callback_data="tests_one_phrase"), 
       types.InlineKeyboardButton(text="📜Повномаштабний тест на рівні📜", callback_data="tests_one_phrase"),
       types.InlineKeyboardButton(text="📜Тест на знання📜", callback_data="tests_one_phrase"),
    ]
]
reply_markups = types.InlineKeyboardMarkup(inline_keyboard=keyboard_test)

keyboard_back = [
    [
        types.InlineKeyboardButton(text="Назад до тестів", callback_data='back_to_tests')
    ]
]
backs = types.InlineKeyboardMarkup(inline_keyboard=keyboard_back)



