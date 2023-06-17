from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

keyboard_remove = ReplyKeyboardRemove()

are_you_sure_rm_id_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Да, отвязать профиль')
).add(
    KeyboardButton('Нет, не нужно')
)


only_cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('cancel')
)

# формируется из ReplyKeyboardMarkup для каждого теста в startup
tests_keyboard = {}
