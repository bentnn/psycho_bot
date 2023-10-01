from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from .const import manage_account_methods
from app import PSYCHO_SITE_URL


button_with_url_to_psycho_syte = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Перейти', url=PSYCHO_SITE_URL)
)


keyboard_remove = ReplyKeyboardRemove()

cancel_button = KeyboardButton('cancel')

are_you_sure_rm_id_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Да, отвязать id')
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

choose_test_kb = InlineKeyboardMarkup(row_width=1)

manage_account_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
for method in manage_account_methods:
    manage_account_kb.add(
        KeyboardButton(method)
    )
manage_account_kb.add(cancel_button)
