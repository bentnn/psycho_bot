from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

keyboard_remove = ReplyKeyboardRemove()

cancel_button = KeyboardButton('cancel')

are_you_sure_rm_id_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Да, отвязать профиль')
).add(
    KeyboardButton('Нет, не нужно')
)


only_cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    cancel_button
)

# формируется из ReplyKeyboardMarkup для каждого теста в startup
tests_keyboard = {}

all_tests_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    cancel_button
).add(
    KeyboardButton('all')
)
