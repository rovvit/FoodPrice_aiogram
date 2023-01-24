import logging
import mysql.connector
from config import API_TOKEN, HELP_COMMANDS
from aiogram import Bot, Dispatcher, executor, types


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
    await message.answer("Бот, который помогает отслеживать динамику цен в магазинах\nАвтор: github.com/rovvit")

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer(HELP_COMMANDS)

@dp.message_handler(commands=['list'])
async def send_welcome(message: types.Message):
    result = "Список магазинов:\n"
    for shop in shopList:
        result = result + shop[1] + '\n'
    print(result)
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    await message.answer(result)

@dp.message_handler(commands=['addShop']) # Функция добавления магазина в БД
async def addShop(message: types.Message):
    await message.answer("Введите название магазина")

@dp.message_handler(commands=['graph']) # Отправка графика
async def show_graph(message: types.Message):
    await bot.send_photo(photo = "https://images.satu.kz/159709422_zaglushka-vnutrennyaya-34.jpg")
    await message.answer("Ответ")



if __name__ == '__main__':
    # Connection to MySQL Server and Building app via token
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="kakashka",
        database="testbase"
    )
    print(mydb)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ShopsDict")
    shopList = []
    for _ in mycursor:
        shopList.append(_)

    executor.start_polling(dp, skip_updates=True)
