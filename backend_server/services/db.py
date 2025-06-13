from sqlalchemy import create_engine
from os import getenv

pg = create_engine(
    f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
)