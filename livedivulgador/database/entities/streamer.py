from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import TIMESTAMP

Base = declarative_base()


class Streamer(Base):
    __tablename__ = "streamers"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    twitch_id = Column(Integer)
    twitter_id = Column(Integer)
    name = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow
    )
