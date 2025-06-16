from sqlalchemy import create_engine, Table,  MetaData, engine, select
from sqlalchemy.exc import IntegrityError, OperationalError
from os import getenv
from functools import wraps
from uuid import UUID
from pydantic import BaseModel

pg = create_engine(
    f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
)
metadata = MetaData()

users = Table('user', metadata, autoload_with=pg)
posts = Table('post', metadata, autoload_with=pg)

class DatabaseError(Exception):
    pass

Connection = engine.Connection

def query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with pg.connect() as conn:
                with conn.begin():
                    return func(conn, *args, **kwargs)
                
        except IntegrityError as e:
            raise DatabaseError(f"Database constraint violated: {e}")
        except OperationalError as e:
            raise DatabaseError(f"Database connection failed: {e}")
        except Exception as e:
            raise DatabaseError(f"Unexpected database error: {e}")

    return wrapper

def database_error_handler(error):
    ...

@query
def create_user(conn: Connection | None, username: str, password: str, email: str):
    return conn.execute(
        users.insert() \
        .values(username=username, password=password, email=email)
    )

class UserResponse(BaseModel):
    id: UUID
    username: str
    password: str
    email: str

@query
def fetch_users(conn: Connection | None) -> list[UserResponse | None]:
    users = conn.execute(
        select(*users.c)
    ).fetchall()
    return [UserResponse.model_validate(row._asdict()) if row else None for row in users]

@query
def fetch_user_by_id(conn: Connection | None, user_id: UUID) -> UserResponse | None:
    row =  conn.execute(
        select(users.c.id, users.c.username, users.c.email) \
        .where(users.c.id == user_id)
    ).fetchone()
    return UserResponse.model_validate(row._asdict()) if row else None

@query
def fetch_user_by_username(conn: Connection | None, username: str) -> UserResponse | None:
    row = conn.execute(
        select(users.c.id, users.c.username, users.c.email, users.c.password) \
        .where(users.c.username == username) \
    ).fetchone()
    return UserResponse.model_validate(row._asdict()) if row else None