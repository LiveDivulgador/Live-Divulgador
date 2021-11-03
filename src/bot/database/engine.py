from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import getenv

load_dotenv()


DATABASE_USER = getenv("DATABASE_USER")
DATABASE_PASSWORD = quote_plus(getenv("DATABASE_PASSWORD"))
DATABASE_HOST = getenv("DATABASE_HOST")
DATABASE_PORT = getenv("DATABASE_PORT")
DATABASE_NAME = getenv("DATABASE_NAME")

args = f"mariadb+mariadbconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(args)

Session = sessionmaker(bind=engine)
