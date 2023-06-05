import app
import aiohttp
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand


async def startup(dispatcher: Dispatcher):
    app.session = aiohttp.ClientSession()
    bot_commands = [
        BotCommand(command="/help", description="Get info about me"),
        BotCommand(command="/qna", description="set bot for a QnA task"),
        BotCommand(command="/chat", description="set bot for free chat")
    ]
    await dispatcher.bot.set_my_commands(bot_commands)


async def shutdown(dispatcher: Dispatcher):
    await app.session.close()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
