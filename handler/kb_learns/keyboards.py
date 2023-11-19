import random,json

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()

for index in range(1, 3):
    builder.button(text=f"Set {index}", callback_data=f"set:{index}")


file_path = 'handler/words.json'

with open(file_path, 'r', encoding='utf-8') as file:
    words_data = json.load(file)


def kb_learn(update: types.Update, context: FSMContext) -> None:
    keyboard = [
        [types.InlineKeyboardButton("Отримати нове слово", callback_data='learn_new_word')],
        [types.InlineKeyboardButton("Отримати словосполучення", callback_data='learn_phrase')],
        [types.InlineKeyboardButton("Отримати відео", callback_data='learn_video')],
    ]
    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)

    update.message.reply_text("Оберіть опцію:", reply_markup=reply_markup)

async def button_click(update: types.Update, context: FSMContext) -> None:
   query = update.callback_query
   option = query.data.get('option')
   user_id = update.from_user.id

   selected_word = random.choice(words_data["words"])

   if option == 'new_word':
       message_text = f'Нове слово: {selected_word["word"]} - {selected_word["translation"]}'
   elif option == 'phrase':
       message_text = f'Фраза: {selected_word["phrase"]}'
   elif option == 'video':
       message_text = f'Відео: {selected_word["video_link"]}'
   else:
       message_text = 'Невідома опція'

   await context.bot.send_message(user_id, text=message_text)

learn_cb = CallbackData('learn', 'new_word', 'phrase', 'video')