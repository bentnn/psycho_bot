from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
import asyncio
import aiohttp
import app
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.start_and_stop import startup, shutdown
from app.keyboards import main_keyboard


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer('Привет! Этот бот позволяет проходить тесты для сайта psycho_test из telegram.\n'
                         'Здесь можно проходить тесты и отслеживать свои результаты')
    await message.answer('Для активации бота вам необходимо зарегистрироваться/авторизоваться на сайте, '
                         'перейти в профиль и ввести ID вашего telegram аккаунта в специальную графу')
    await message.answer('Ваш ID:')
    await message.answer(message.from_user.id, reply_markup=main_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
