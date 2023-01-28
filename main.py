import logging
import mysql.connector
from config import API_TOKEN, HELP_COMMANDS, BOT_USER, BOT_PASSWORD, BOT_DB
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup ,InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
# from aiogram.types import FSInputFile


# Configure logging
logging.basicConfig(
    filename="LOG.LOG",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
startButton = KeyboardButton(text='/register')
kb.add(startButton)

# ikb = InlineKeyboardMarkup()
# buttonHelp = InlineKeyboardButton(text='help', url="google.com")
# buttonList = InlineKeyboardButton(text='list', url="yahoo.com")
# ikb.add(buttonHelp).add(buttonList)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    await message.answer(text="Бот, который помогает отслеживать динамику цен в магазинах",
                         reply_markup=kb)
    # await bot.send_message(chat_id=message.chat.id,
    #                        text="Бот, который помогает отслеживать динамику цен в магазинах",
    #                        reply_markup=ikb
    #                        )

@dp.message_handler(commands='register')
async def register(message: types.Message):
    city_ikb = InlineKeyboardMarkup()
    buttonAstana = InlineKeyboardButton(text="Астана", callback_data="Астана")
    city_ikb.add(buttonAstana)
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
    path="C:/Users/Виталий/PycharmProjects/FoodPrice_aiogram/Blank.png"
    # await bot.send_photo(chat_id=message.chat.id,
    #                      photo="https://i.ytimg.com/vi/OOFGdRmN70k/maxresdefault.jpg",
    #                      caption="Заглушка")
    await bot.send_message(chat_id=message.chat.id,
                           text="text")
    # image=FSInputFile("Blank.png")
    await bot.send_photo(
                         chat_id=message.chat.id,
                         photo=image)


    # await message.delete()
    # await message.delete()
    # await message.answer("Ответ")
    # await bot.send_photo(
    #     photo="Blank.png",
    #     caption="Заглушка")

@dp.callback_query_handler()
async def callback_register(callback: types.CallbackQuery):
    # await callback.answer(text="Кнопка нажалась")
    city = callback.data
    chatId = callback.message.chat.id
    mycursor.execute("SELECT uc.user_id, c.name FROM UserCity uc INNER JOIN Cities c ON uc.city_id = c.id WHERE uc.user_id = %s", (chatId,))
    row_count = mycursor.rowcount
    if row_count > 0:
        result = []
        for _ in mycursor:
            result.append(_)
        await callback.message.answer(text="Вы уже выбрали город "+result[0][1])
    else:
        print("Регистрация пользователя "+str(callback.message.chat.id)+" в городе "+city)
        mycursor.execute("SELECT id FROM Cities WHERE name = %s LIMIT 1", (city,))
        # print(mycursor)
        cityid = mycursor.fetchone()
        cityid = cityid[0]
        # cityid = mycursor
        # print(cityid)
        mycursor.execute("INSERT INTO UserCity (user_id, city_id) VALUES (%s, %s)", (chatId, cityid))
        mydb.commit()
        await callback.message.delete()
        await callback.message.answer(text="Ваш город - " + city)



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
    mycursor.execute("SELECT * FROM ShopsDict")
    shopList = []
    for _ in mycursor:
        shopList.append(_)

    executor.start_polling(dp, skip_updates=True)
