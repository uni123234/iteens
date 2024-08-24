import random

from aiogram import types

from ...config import WORDS


keyboard = [
    [
        types.InlineKeyboardButton(
            text="📜Отримати нове слово📜", callback_data="learn_new_word"
        )
    ]
]
reply_markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_random_word():

    random_word = random.choice(WORDS["words"])

    word = random_word["word"]
    translation = random_word["translation"]
    phrase = random_word["phrase"]

    inline_btn = [
        [
            types.InlineKeyboardButton(
                text="📜Отримати нове слово📜", callback_data="learn_new_word"
            )
        ]
    ]

    inline_kb = types.InlineKeyboardMarkup(inline_keyboard=inline_btn)

    return [f"Слово: {word}\nПереклад: {translation}\nФраза: {phrase}", inline_kb]
