from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import getenv

load_dotenv()


user_db = getenv("user_db")
passwd_db = getenv("passwd_db")
host_db = getenv("host_db")
port_db = getenv("port_db")


engine = create_engine(
    "postgresql://{}:{}@{}:{}/streamers".format(
        user_db, quote_plus(passwd_db), host_db, port_db
    )
)

Session = sessionmaker(bind=engine, future=True)
