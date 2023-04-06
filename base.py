import aiosqlite 
from aiogram import types

async def conn():
    return await aiosqlite.connect('data.db')


async def checkUser(user_id):
    db = await conn()
    sql = await db.cursor()
    await sql.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = await sql.fetchone()
    if result == None:
        _return =0
    else:
        _return = 1
    await db.close()
    return _return

async def insertUser(user_id):
    db = await conn()
    sql = await db.cursor()
    await sql.execute("INSERT INTO users VALUES (?)", (user_id,))
    await db.commit()
    await db.close()
    return 1

async def getCategories(user_id):
    db = await conn()
    sql = await db.cursor()
    await sql.execute("SELECT * FROM categories WHERE user_id = ?", (user_id,))
    result = await sql.fetchall()
    if result == None:
        await db.commit()
        await db.close()
        return 0
    else:
        await db.commit()
        await db.close()
        return result

async def genCategories(user_id):
    db = await conn()
    sql = await db.cursor()
    categories = await getCategories(user_id = user_id)
    if categories != None:
        key = types.InlineKeyboardMarkup()
        for i in categories:
            key.add(types.InlineKeyboardButton(text=f"{i[2]}", callback_data=f'category_{i[0]}'))
        key.add(types.InlineKeyboardButton(text = 'Без категории', callback_data='none_categor'))
        key.add(types.InlineKeyboardButton(text='Новая категория', callback_data='new_categor'))
        await db.commit()
        await db.close()
        return key
    else:
        await db.commit()
        await db.close()
        return 0

async def genNonCategoryFiles(user_id):
    db = await conn()
    sql = await db.cursor()
    await sql.execute("SELECT * FROM files WHERE user_id = ? and category = ?", (user_id, 0))
    result = await sql.fetchall()
    await db.commit()
    await db.close()
    return result

async def newCategories(user_id, title='test'):
    db = await conn()
    sql = await db.cursor()
    await sql.execute("INSERT INTO categories VALUES (NULL, ?, ?)", (user_id, title))
    await db.commit()
    await db.close()

async def new_file(user_id, title, file_id, file_name_id):
    db = await conn()
    sql = await db.cursor()
    await sql.execute("INSERT INTO files VALUES (NULL, ?, ?, ?, ?, ?)", (user_id, file_id, title, 0, file_name_id))
    await db.commit()
    await db.close()

async def getFile(file_id):
    db = await conn()
    sql = await db.cursor()
    await sql.execute("SELECT * FROM files WHERE id = ?", (file_id,))
    result = await sql.fetchone()
    await db.commit()
    await db.close()
    return result

async def changeCategory(file_id, category):
    db = await conn()
    sql = await db.cursor()
    await sql.execute("UPDATE files SET category = ? WHERE id = ?", (category, file_id,))
    await db.commit()
    await db.close()

async def getFileswithCategory(user_id, category):
    db = await conn()
    sql = await db.cursor()
    await sql.execute("SELECT * FROM files WHERE category = ? and user_id = ?", (category, user_id))
    result = await sql.fetchall()
    await db.commit()
    await db.close()
    return result 

async def newCategory(user_id, title):
    db = await conn()
    sql = await db.cursor()
    await sql.execute("INSERT INTO categories VALUES (NULL, ?, ?)", (user_id, title))
    await db.commit()
    await db.close()