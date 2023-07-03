import app
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
from .base_funcs import send_psycho_site_request
from app import PSYCHO_SITE_URL
from .keyboards import tests_keyboard, all_tests_keyboard, cancel_button
import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def startup(dispatcher: Dispatcher):
    logging.info('Start startup')
    bot_commands = [
        BotCommand(command="/start", description="Информация о боте"),
        BotCommand(command="/run_test", description="Пройти тест"),
        BotCommand(command="/stats", description="Посмотреть статистику по тестам"),
        BotCommand(command="/check_id", description="Проверить связку бота и профиля на сайте"),
        BotCommand(command="/rm_id", description="Отвязать бота от аккаунта"),
    ]
    # dispatcher.middleware.setup(LoggingMiddleware())
    (status, tests), *_ = await asyncio.gather(
        send_psycho_site_request('GET', 'tests', return_json=True),
        dispatcher.bot.set_my_commands(bot_commands)
    )
    if status != 200:
        raise RuntimeError(f'Failed to get tests: {tests}')
    logging.info(f'Тесты выгружены в количестве {len(tests)}')
    keyboards = {}
    for test_name, test_info in tests.items():
        new_answers = {ans['name']: ans['value'] for ans in test_info['answers']}
        app.normal_test_name_to_technical[test_info['name']] = test_name
        all_tests_keyboard.add(KeyboardButton(test_info['name']))
        test_info['answers'] = new_answers
        answers = tuple(new_answers.keys())

        if answers in keyboards:
            this_test_keyboard = keyboards[answers]
        else:
            this_test_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            for i in answers:
                this_test_keyboard.add(KeyboardButton(i))
            this_test_keyboard.add(cancel_button)
            keyboards[answers] = this_test_keyboard
        tests_keyboard[test_name] = this_test_keyboard

        for i in range(len(test_info['questions'])):
            test_info['questions'][i] = f'{i + 1}. {test_info["questions"][i]}'
    logging.info(f'Клавиатуры ответов на тесты сформированы в количестве {len(keyboards)}')
    app.psycho_tests = tests
    logging.info('Finish startup')


async def shutdown(dispatcher: Dispatcher):
    logging.info('Start shutdown')
    await app.session.close()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logging.info('Finish shutdown')
