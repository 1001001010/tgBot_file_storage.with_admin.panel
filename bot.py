from aiogram import types, executor, Dispatcher, Bot
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
import datetime
import base as db
import random
import re
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram import types
# MODULES

import keyboards as key
from config import *
# FILES

global link

conn = sqlite3.connect('data.db')
cur = conn.cursor()

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

class newfiles(StatesGroup):
    title = State()
    file = State()
class newcategory(StatesGroup):
    title = State()

admin_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
adm_file = types.KeyboardButton(text="📁Файлы")
adm_white_list = types.KeyboardButton(text="📄Белый лист")
history_file = types.KeyboardButton(text="🕓История выгрузки")
admin_menu.add(adm_file, adm_white_list)
admin_menu.add(history_file)

file_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
add_file = types.KeyboardButton(text = "➕Добавить файлы")
back = types.KeyboardButton(text = "⏪Назад")
file_menu.add(add_file)
file_menu.add(back)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
        if message.from_user.id == admin_id:
          await bot.send_message(message.from_user.id, f'Админ меню: ', reply_markup=admin_menu)
        else:
          user_to = message.from_user.id
          cur = conn.cursor()
          info_user_to = cur.execute("SELECT * FROM list WHERE tg_id = " + str(user_to)).fetchall()
          if len(info_user_to) > 0:
              cur = conn.cursor()
              entry = cur.fetchone()
              dt_registr = datetime.datetime.now()
              args = message.get_args()
              reference = str(decode_payload(args))
              sqlite_select_query = f"""SELECT file_id from files WHERE file_name_id = {reference}"""
              cur.execute(sqlite_select_query)
              records = str(cur.fetchall())
              records = str(records.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace("'", '').replace(",", ''))
              user = (f'{message.from_user.id}', f'{dt_registr}', '1', f'{records}')
              cur.execute("INSERT INTO user VALUES(?, ?, ?, ?);", user)
              conn.commit()
              args = message.get_args()
              reference = str(decode_payload(args))
              sqlite_select_query = f"""SELECT file_id from files WHERE file_name_id = {reference}"""
              cur.execute(sqlite_select_query)
              records = str(cur.fetchall())
              records = str(records.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace("'", '').replace(",", ''))
              await message.answer_document(records)
          else: 
              await bot.send_message(message.from_user.id, f'У вас нет доступа')

@dp.message_handler(text = ["📁Файлы"])
async def file_start(message: types.Message):
    if message.from_user.id == admin_id:
      await bot.send_message(message.from_user.id, f'Файловое меню', reply_markup=file_menu)

@dp.message_handler(text = ["🕓История выгрузки"])
async def file_start(message: types.Message):
    if message.from_user.id == admin_id:
        await bot.send_message(message.from_user.id,"Смотри все выгрузки в терминале\cmd")
        cur.execute("SELECT * FROM user;")
        all_results = cur.fetchall()
        for row in all_results:
            print("ID:", row[0])
            print("Время выгрузки:", row[1])
            print("В белом листе:", row[2])
            print("Выгружаемый файл", row[3], end="\n\n")
        # print(f"{all_results}\n")

@dp.message_handler(text = ["⏪Назад"])
async def main_menu(message: types.Message):
    if message.from_user.id == admin_id:
      await bot.send_message(message.from_user.id, f'Админ меню: ', reply_markup=admin_menu)
    else:
      await bot.send_message(message.from_user.id, f'Главное меню: ')

@dp.message_handler(text = ["📄Белый лист"])
async def white(message: types.Message):
    if message.from_user.id == admin_id:
      await bot.send_message(message.from_user.id, f'Введите user ID: ')
      @dp.message_handler()
      async def white_list(msg: types.Message):
          b = msg.text
          await bot.send_message(msg.from_user.id, f"Пользователь (ID - {msg.text})\nУспешно добавлен в белый лист")
          cur = conn.cursor()
          entry = cur.fetchone()
          dt_list = datetime.datetime.now()
          user = (f'{b}', f'{dt_list}')
          cur.execute("INSERT INTO list VALUES(?, ?);", user)
          conn.commit()
    else:
      await bot.send_message(message.from_user.id, f'У вас нет доступа') 

@dp.message_handler(text = ["➕Добавить файлы"])
async def white(message: types.Message):
    if message.from_user.id == admin_id:
      await bot.send_message(message.from_user.id, f'Главное меню: ', reply_markup=key.menu)
    else:
       await bot.send_message(message.from_user.id, f'Нет доступа', reply_markup=key.menu)
@dp.callback_query_handler()
async def call_handler(call: types.CallbackQuery):
    if call.data == 'files':
        categories = await db.genCategories(call.from_user.id)
        if categories != 0:
            await bot.send_message(call.from_user.id, f'Все Категории:', reply_markup=categories)
        else:
            await bot.send_message(call.from_user.id, f'Категорий нету!')

    if call.data == 'new_file':
        await bot.send_message(call.from_user.id, f'Введите название для проекта')
        await newfiles.title.set()
    if 'sendfile' in call.data:
        file_id = call.data.split('|')[1]
        file = await db.getFile(file_id)
        link = await get_start_link(str(f"{file[5]}"), encode=True)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Сменить категорию', callback_data=f'swap|{file_id}')
        btn2 = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(btn1, btn2)
        await bot.send_document(call.from_user.id, file[2], caption=f'Название проекта: {file[3]}\nАйди - <code>{file[5]}</code>\nСсылка на файл - <code>{link}</code>', reply_markup=keyboard, parse_mode="HTML")
        # print(file[5])
    if 'back' in call.data:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        files = await db.genNonCategoryFiles(user_id = call.from_user.id)
        keyboard = types.InlineKeyboardMarkup()
        keyboard2 = types.InlineKeyboardMarkup()
        for i in files:
            keyboard.add(
            types.InlineKeyboardButton(text = f'{i[3]}', callback_data=f'sendfile|{i[0]}')
            # types.InlineKeyboardButton(text = 'Следующая странциа', callback_data=f'sendfile|{i[0]}')
            )
        keyboard2.add(
            types.InlineKeyboardButton(text = "next", callback_data="and")
        )
    if call.data == 'new_categor':
        await bot.send_message(call.from_user.id, f'Введите название категории')
        await newcategory.title.set()
    if call.data == 'none_categor':
        files = await db.genNonCategoryFiles(user_id = call.from_user.id)
        print(files)
        keyboard = types.InlineKeyboardMarkup()
        for i in files:
            keyboard.add(
                types.InlineKeyboardButton(text = f'{i[3]}', callback_data=f'sendfile|{i[0]}')
            )
        await bot.send_message(call.from_user.id, 'Файлы без категории: ', reply_markup=keyboard)
    if 'dellete' in call.data:
        await bot.send_message(call.from_user.id, f'Введите айди файла: ')
        @dp.message_handler()
        async def del_files (msg: types.Message):
            a = int(msg.text)
            await bot.send_message(msg.from_user.id,f"Удален файл - {msg.text}")
            sql_delete_query = (f"""DELETE from files where file_name_id = {a}""")
            cur.execute(sql_delete_query)
            conn.commit()
    if 'swap' in call.data:
        file_id = call.data.split('|')[1]
        categories = await db.getCategories(user_id = call.from_user.id)
        print(categories)
        keyboard = types.InlineKeyboardMarkup()
        for i in categories:
            keyboard.add(types.InlineKeyboardButton(text=i[2], callback_data=f'to|{file_id}|{i[0]}'))
        await bot.send_message(call.from_user.id, f'Выберите категорию: ', reply_markup=keyboard)

    if 'to' in call.data:
        file_id = call.data.split('|')[1]
        category = call.data.split('|')[2]
        await db.changeCategory(file_id, category)
        await bot.send_message(call.from_user.id, f'Вы сменили категорию у файла!')

    if 'category' in call.data:
        category_id = call.data.split('_')[1]
        files = await db.getFileswithCategory(user_id = call.from_user.id, category=category_id)
        keyboard = types.InlineKeyboardMarkup()
        for i in files:
            keyboard.add(types.InlineKeyboardButton(text=f'{i[3]}', callback_data=f'sendfile|{i[0]}'))
        await bot.send_message(call.from_user.id, f'Категория:', reply_markup=keyboard)

@dp.message_handler(state = newcategory.title)
async def state_newcategory(message: types.Message, state: FSMContext):
    await state.update_data(title = message.text)
    await db.newCategory(user_id=message.from_user.id, title=message.text)
    await bot.send_message(message.from_user.id, f'Категория создана!')
    await state.finish()

@dp.message_handler(state = newfiles.title)
async def state_newfiles(message: types.Message, state: FSMContext):
    await state.update_data(title = message.text)
    await bot.send_message(message.from_user.id, f'Отправьте файлы: ')
    await newfiles.file.set()

@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state = newfiles.file)
async def state_files(message: types.Message, state: FSMContext):
    l = random.randint(0, 999999999)
    file_id = message.document.file_id
    data = await state.get_data()
    title = data['title']
    await db.new_file(user_id = message.from_user.id, title = title, file_id = file_id, file_name_id=l)
    await state.finish()
    await bot.send_message(message.from_user.id, f'Вы добавили новый файл!', parse_mode="HTML")
    



executor.start_polling(dp)
