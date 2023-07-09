import aiosqlite
from sqlalchemy import select
from .models import Base, UserMsgs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db import db_confs
import logging


async def create_db():
    db_connection = await aiosqlite.connect('db.sqlite3')
    engine = create_async_engine(
        "sqlite+aiosqlite:///db.sqlite3",
        echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        result = await conn.execute(select(UserMsgs))
        logging.info(f'\tDB now has {len(result.fetchall())} object(s) of UserMsgs')
    db_session = async_sessionmaker(engine, expire_on_commit=False)
    db_confs.set_engine(engine)
    db_confs.set_session(db_session)
    db_confs.set_connection(db_connection)
