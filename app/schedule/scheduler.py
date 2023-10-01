import asyncio
import aioschedule
from aiogram.dispatcher import Dispatcher
from app import psycho_tests, days_to_restart_schedule
from app.base_funcs import send_psycho_site_request
from random import randint
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging


class Scheduler:

    def __init__(self):
        self._dispatcher: Dispatcher = None
        self._schedule_task: asyncio.Task = None
        self._tests_to_run: list = None
        self._current_test: str = None
        self._days_to_restart = 0

    def __del__(self):
        self.remove_schedule_if_exist()

    def set_dispatcher(self, dispatcher):
        self._dispatcher = dispatcher

    async def start_sending(self):
        try:
            logging.info('Start new everyday test')
            all_user_ads = await send_psycho_site_request(method='get', url='telegramid/all_ids', return_json=True)
            all_user_ads = all_user_ads[1]
            button = InlineKeyboardMarkup()
            button.add(
                InlineKeyboardButton(text='Начать тест', callback_data=f'start_test:{self._current_test}')
            )
            msg = 'Привет!\nРекомендую сегодня пройти следующий тест:\n' + psycho_tests[self._current_test]['name']
            await asyncio.gather(
                *(
                    self._dispatcher.bot.send_message(chat_id=user_id, text=msg, reply_markup=button)
                    for user_id in all_user_ads
                )
            )
        except Exception as e:
            logging.error(f'Ошибка при запуске старта ежедневного теста: {e}')

    async def continue_sending(self):
        pass

    async def run_schedule(self):
        logging.info('Run everyday action')
        if self._days_to_restart:
            self._days_to_restart -= 1
            await self.continue_sending()
        else:
            if not self._tests_to_run:
                self._tests_to_run = list(psycho_tests)
            self._current_test = self._tests_to_run.pop(randint(0, len(self._tests_to_run) - 1))
            self._days_to_restart = days_to_restart_schedule - 1
            await self.start_sending()

    async def everyday_schedule(self, new_time: str) -> None:
        """

        :param new_time: like "12:00"
        """
        aioschedule.every().day.at(new_time).do(self.run_schedule)
        await self.run_schedule()
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)

    def create_schedule(self, new_time: str):
        self.remove_schedule_if_exist()
        self._schedule_task = asyncio.create_task(self.everyday_schedule(new_time))

    def remove_schedule_if_exist(self):
        if self._schedule_task:
            self._schedule_task.cancel()
