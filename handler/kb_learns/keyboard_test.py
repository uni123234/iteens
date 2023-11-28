from aiogram import types

keyboard_test = [
    
       [types.InlineKeyboardButton(text="📜Тест по одному слову📜", callback_data="tests_one_word")],
       [types.InlineKeyboardButton(text="📜Тест на часи📜", callback_data="tests_one_phrase")],
       [types.InlineKeyboardButton(text="📜Повномаштабний тест на рівні📜", callback_data="yes")],
       [types.InlineKeyboardButton(text="📜Тест на знання📜", callback_data="None")],
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


def dynamic_reply_db(answers: list):
     return types.InlineKeyboardMarkup(
         inline_keyboard=[
             [types.InlineKeyboardButton(text=answer, callback_data=answer) for answer in answers] 
         ]
     )


keyboard_l = [ 
    [types.InlineKeyboardButton(text='Так', callback_data='yes')],
    [types.InlineKeyboardButton(text='Нi', callback_data='no')],
]
reply_markupe = types.InlineKeyboardMarkup(inline_keyboard=keyboard_l)


keyboard__lvl = [
    [types.InlineKeyboardButton(text='a1-с1', callback_data='a1')],
]
reply_markup_lvl = types.InlineKeyboardMarkup(inline_keyboard=keyboard__lvl)
