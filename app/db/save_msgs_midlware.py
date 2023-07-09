from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import async_session
from app.db import db_confs
from .models import UserMsgs
from datetime import datetime


class SaveMessagesMiddleware(BaseMiddleware):

    async def on_process_message(self, message: Message, data: dict):
        async with db_confs.db_session() as session:
            async with session.begin():
                session.add(UserMsgs(user_id=message.from_user.id, msg=message.text, datetime=datetime.now()))
