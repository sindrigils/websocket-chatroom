from sqlalchemy import create_engine
from dotenv import load_dotenv

from os import environ

load_dotenv()

username = environ.get("DB_USERNAME")
password = environ.get("DB_PASSWORD")
host = environ.get("DB_HOST")
port = environ.get("DB_PORT")
database = environ.get("DB_NAME")

engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")
