import asyncio
import aioschedule
from datetime import datetime, timedelta
import time
from app import psycho_tests, days_to_restart_schedule


class Scheduler:

    _dispatcher = None
    _schedule_task: asyncio.Task = None
    _tests_to_run = set()

    def set_dispatcher(self, dispatcher):
        self._dispatcher = dispatcher

    async def start_sending(self):
        pass

    async def continue_sending(self):
        pass

    async def run_schedule(self):
        pass

    async def everyday_schedule(self, new_time: str) -> None:
        """

        :param new_time: like "12:00"
        """
        # time.strftime()
        # to_next_doing = time.fromisoformat(new_time) - datetime.now().time()
        aioschedule.every().day.at(new_time).do(self.run_schedule)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(60)

    def create_schedule(self, new_time: str):
        self.remove_schedule_if_exist()
        self._schedule_task = asyncio.create_task(self.everyday_schedule(new_time))

    def remove_schedule_if_exist(self):
        if self._schedule_task:
            self._schedule_task.cancel()
