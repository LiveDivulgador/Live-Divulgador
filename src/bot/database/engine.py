from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import getenv

load_dotenv()


user_db = getenv("DATABASE_USER")
passwd_db = getenv("DATABASE_PASSWORD")
host_db = getenv("DATABASE_HOST")
port_db = getenv("DATABASE_PORT")


engine = create_engine(
    "postgresql://{}:{}@{}:{}/streamers".format(
        user_db, quote_plus(passwd_db), host_db, port_db
    )
)

Session = sessionmaker(bind=engine, future=True)
