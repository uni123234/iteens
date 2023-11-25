from aiogram import types

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

def keyboard_t(word1,word2,word3,word4):
    keyboard_l = [ 
        [types.InlineKeyboardButton(text=word1, callback_data=word1)],
        [types.InlineKeyboardButton(text=word2, callback_data=word2)], 
        [types.InlineKeyboardButton(text=word3, callback_data=word3)], 
        [types.InlineKeyboardButton(text=word4, callback_data=word4)],
    ]
    reply_markupu = types.InlineKeyboardMarkup(inline_keyboard=keyboard_l)

    return reply_markupu

def keyboard_test_a(word1,word2,word3,word4,word5,word6,word7):
    keyboard_l = [ 
        [types.InlineKeyboardButton(text=word1, callback_data=word1)],
        [types.InlineKeyboardButton(text=word2, callback_data=word2)], 
        [types.InlineKeyboardButton(text=word3, callback_data=word3)], 
        [types.InlineKeyboardButton(text=word4, callback_data=word4)],
        [types.InlineKeyboardButton(text=word4, callback_data=word5)],
        [types.InlineKeyboardButton(text=word4, callback_data=word6)],
        [types.InlineKeyboardButton(text=word4, callback_data=word7)],
    ]
    reply_markupe = types.InlineKeyboardMarkup(inline_keyboard=keyboard_l)

    return reply_markupe