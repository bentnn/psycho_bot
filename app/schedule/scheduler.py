import asyncio
import aioschedule
from datetime import datetime, timedelta
import time


class Scheduler:

    _dispatcher = None
    _schedule_task = None

    def set_dispatcher(self, dispatcher):
        self._dispatcher = dispatcher

    async def run_schedule(self):
        pass

    async def everyday_schedule(self, new_time: str) -> None:
        """

        :param new_time: like "12:00"
        """
        # time.strftime()
        # to_next_doing = time.fromisoformat(new_time) - datetime.now().time()
        to_next_doing = time.strptime("12:00", "%H:%M").count()
        aioschedule.every().day.at(new_time).do(self.run_schedule)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(360)
