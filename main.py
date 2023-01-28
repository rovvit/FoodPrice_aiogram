import logging
import mysql.connector
from config import API_TOKEN, HELP_COMMANDS, BOT_USER, BOT_PASSWORD, BOT_DB
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup ,InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards import register_kb, main_ikb

# Configure logging
logging.basicConfig(
    filename="LOG.LOG",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(text="Бот, который помогает отслеживать динамику цен в магазинах",
                         reply_markup=register_kb)

@dp.message_handler(commands='register')
async def register(message: types.Message):
    chatId = message.chat.id
    mycursor.execute("SELECT uc.user_id, c.name FROM UserCity uc INNER JOIN Cities c ON uc.city_id = c.id WHERE uc.user_id = %s", (chatId,))
    row_count = mycursor.rowcount
    if row_count > 0:
        await message.answer(text="Выберите действие",
                             reply_markup=main_ikb)
    elif row_count == 0:
        city_ikb = InlineKeyboardMarkup() # Создание клавиатуры с городами
        mycursor.execute("SELECT name FROM Cities")
        for city in mycursor:
            city_ikb.add(InlineKeyboardButton(text=str(city[0]),
                                               callback_data=str(city[0])))
        await message.answer(text="Выберите город",
                             reply_markup=city_ikb
                             )


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer(HELP_COMMANDS)

@dp.message_handler(commands=['list'])
async def send_list(message: types.Message):
    result = "Список магазинов:\n"
    for shop in shopList:
        result = result + shop[1] + '\n'
    print(result)
    await bot.send_message(chat_id=message.chat.id,
                           text=result
                           )

@dp.message_handler(commands=['addShop']) # Функция добавления магазина в БД
async def addShop(message: types.Message):
    await message.answer("Введите название магазина")

@dp.message_handler(commands=['graph']) # Отправка графика
async def show_graph(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="text")
    # await bot.send_photo(
    #                      chat_id=message.chat.id,
    #                      photo=image)

@dp.callback_query_handler(text='AddShop')
async def add_shop_callback(callback: types.CallbackQuery):
    await callback.message.answer(text="Введите название магазина")

@dp.callback_query_handler(text='AddPrice')
async def add_price_callback(callback: types.CallbackQuery):
    shops_ikb = InlineKeyboardMarkup(row_width=2)
    mycursor.execute("SELECT name FROM ShopsDict WHERE City_id = (SELECT city_id FROM UserCity where user_id = %s)", (callback.message.chat.id,))
    for shop in mycursor:
         shops_ikb.add(InlineKeyboardButton(text=str(shop[0]),
                                           callback_data=str(shop[0])))
    await callback.message.answer(text="Выберите магазин",
                                  reply_markup=shops_ikb)

@dp.callback_query_handler()
async def callback_register(callback: types.CallbackQuery):
    if callback.data in cities:
        city = callback.data
        chat_id = callback.message.chat.id
        mycursor.execute("SELECT uc.user_id, c.name FROM UserCity uc INNER JOIN Cities c ON uc.city_id = c.id WHERE uc.user_id = %s", (chat_id,))
        row_count = mycursor.rowcount
        if row_count > 0:
            result = []
            for _ in mycursor:
                result.append(_)
            await callback.message.answer(text="Вы уже выбрали город "+result[0][1])
        else:
            print("Регистрация пользователя "+str(callback.message.chat.id)+" в городе "+city)
            mycursor.execute("SELECT id FROM Cities WHERE name = %s LIMIT 1", (city,))
            cityid = mycursor.fetchone()[0]
            mycursor.execute("INSERT INTO UserCity (user_id, city_id) VALUES (%s, %s)", (chat_id, cityid))
            mydb.commit()
            await callback.message.delete()
            await callback.message.answer(text="Ваш город - " + city,
                                          reply_markup=main_ikb)
    else:
        mycursor.execute("SELECT name FROM ShopsDict WHERE City_id = (SELECT city_id FROM UserCity WHERE user_id = %s)", (callback.message.chat.id,))
        shop_list = []
        for _ in mycursor:
            shop_list.append(str(_[0]))
    if callback.data in shop_list:
        await callback.message.answer(text=callback.data) #TODO создать таблицу с ценами и написать инсерт отсюда


@dp.callback_query_handler()
async def call_back_blank(callback: types.CallbackQuery):
    await callback.message.answer(text="Ничего не поймалось")



if __name__ == '__main__':
    # Connection to MySQL Server and Building app via token
    mydb = mysql.connector.connect(
        host="localhost",
        user=BOT_USER,
        password=BOT_PASSWORD,
        database=BOT_DB
    )
    print(mydb)
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT name FROM Cities")
    cities = []
    for _ in mycursor:
        cities.append(str(_[0]))
    print(cities)
    executor.start_polling(dp, skip_updates=True)
