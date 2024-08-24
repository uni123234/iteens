"""
This module defines inline keyboards for various tests in the Telegram bot.

It includes predefined keyboards and functions for generating dynamic keyboards.
"""

from aiogram import types

# Predefined keyboards
keyboard_test = [
    [
        types.InlineKeyboardButton(
            text="📜Тест по одному слову📜", callback_data="tests_one_word"
        )
    ],
    [
        types.InlineKeyboardButton(
            text="📜Тест на часи📜", callback_data="tests_one_phrase"
        )
    ],
    [
        types.InlineKeyboardButton(
            text="📜Повномаштабний тест на рівні📜", callback_data="yes"
        )
    ],
]
reply_markups = types.InlineKeyboardMarkup(inline_keyboard=keyboard_test)

keyboard_back = [
    [types.InlineKeyboardButton(text="Назад до тестів", callback_data="back_to_tests")]
]
backs = types.InlineKeyboardMarkup(inline_keyboard=keyboard_back)


def keyboard_t(word1: str, word2: str, word3: str, word4: str) -> types.InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup with four buttons.

    Args:
        word1 (str): Text and callback data for the first button.
        word2 (str): Text and callback data for the second button.
        word3 (str): Text and callback data for the third button.
        word4 (str): Text and callback data for the fourth button.

    Returns:
        types.InlineKeyboardMarkup: The created inline keyboard markup.
    """
    # Renamed variable to avoid conflict
    keyboard_buttons = [
        [types.InlineKeyboardButton(text=word1, callback_data=word1)],
        [types.InlineKeyboardButton(text=word2, callback_data=word2)],
        [types.InlineKeyboardButton(text=word3, callback_data=word3)],
        [types.InlineKeyboardButton(text=word4, callback_data=word4)],
    ]
    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    return reply_markup


def dynamic_reply_db(answers: list) -> types.InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup based on a list of answers.

    Args:
        answers (list): List of answers where each answer is used as text and callback data for a button.

    Returns:
        types.InlineKeyboardMarkup: The created inline keyboard markup.
    """
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text=answer, callback_data=answer)
                for answer in answers
            ]
        ]
    )


# Predefined keyboards for responses
response_buttons = [
    [types.InlineKeyboardButton(text="Так", callback_data="yes")],
    [types.InlineKeyboardButton(text="Нi", callback_data="no")],
]
reply_markup_response = types.InlineKeyboardMarkup(inline_keyboard=response_buttons)

level_buttons = [
    [types.InlineKeyboardButton(text="a1-с1", callback_data="a1")],
]
reply_markup_level = types.InlineKeyboardMarkup(inline_keyboard=level_buttons)
