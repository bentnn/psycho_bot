import app
import asyncio
from aiogram.dispatcher import Dispatcher
from .bot_commands_list import bot_commands
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
from .base_funcs import send_psycho_site_request
from .keyboards import tests_keyboard, all_tests_keyboard, cancel_button, choose_test_kb
import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from app.db.create_db import create_db
from app.db import db_confs
from app.schedule import scheduler_object


async def startup(dispatcher: Dispatcher):
    logging.info('Start startup')
    create_db_task = asyncio.create_task(create_db())
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
        choose_test_kb.add(InlineKeyboardButton(test_info['name'], callback_data=test_name))
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

    scheduler_object.create_schedule(app.everyday_test_time)
    logging.info('Schedule created')

    await create_db_task

    logging.info('Finish startup')


async def shutdown(dispatcher: Dispatcher):
    async def close_storage():
        await dispatcher.storage.close()
        await dispatcher.storage.wait_closed()
    logging.info('Start shutdown')
    scheduler_object.remove_schedule_if_exist()
    await asyncio.gather(
        close_storage(),
        app.session.close(),
        db_confs.engine.dispose(),
        db_confs.db_connection.close()
    )
    logging.info('Finish shutdown')
