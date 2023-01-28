from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

register_kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
startButton = KeyboardButton(text='/register')
register_kb.add(startButton)


main_ikb = InlineKeyboardMarkup(row_width=2)
add_shop = InlineKeyboardButton(text="Добавить магазин",
                                callback_data="AddShop")
add_price = InlineKeyboardButton(text="Внести цены",
                                 callback_data="AddPrice")
main_ikb.add(add_shop).add(add_price)

