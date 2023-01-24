import logging
import mysql.connector

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5633933532:AAFHjtou1on6oImwMEHvsa9wWYt-Ww1KmTs'

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
    await message.reply("Бот, который помогает отслеживать динамику цен в магазинах\nАвтор: github.com/rovvit")

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Здесь будет справка")

@dp.message_handler(commands=['list'])
async def send_welcome(message: types.Message):
    result = "Список магазинов:\n"
    for shop in shopList:
        result = result + shop[1] + '\n'
    print(result)
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    await message.reply(result)


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
