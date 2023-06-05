from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Пройти тест')
).add(
    KeyboardButton('Проверить привязку к сайту')
)
