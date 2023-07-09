from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserMsgs(Base):
    __tablename__ = "user_messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    msg = Column(Text)
    datetime = Column(DateTime)
