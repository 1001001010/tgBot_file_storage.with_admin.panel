from aiogram import types 

import base as db

menu = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton(
    text = '📁Файлы',
    callback_data = 'files'
)
btn2 = types.InlineKeyboardButton(
    text = '➕Новый файл',
    callback_data = 'new_file'
)
menu.add(btn1, btn2)


menu2 = types.InlineKeyboardMarkup()
bt3 = types.InlineKeyboardButton(
    text = '⏪Назад',
    callback_data = 'back'
)
menu2.add(bt3)

menu3 = types.InlineKeyboardMarkup()
bt4 = types.InlineKeyboardButton(
    text = '⏪Назад',
    callback_data = 'back2'
)
menu3.add(bt4)

get_link_ok = types.InlineKeyboardMarkup()
ok1 = types.InlineKeyboardButton(
    text = '👌ОК',
    callback_data = 'ok'
)
get_link_ok.add(ok1)

