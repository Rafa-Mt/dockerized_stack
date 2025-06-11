from flask import Flask, jsonify
from redis import Redis
from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine
from services.routes import routes

load_dotenv()  

app = Flask(__name__)

redis = Redis(
    host = "redis", 
    port = 6379, 
    db = 0,
    decode_responses=True
)

sqlalchemy = create_engine(
    f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
)

redis.hset('object_test', mapping={"Hello": "World", "Foo": "Bar"})

if __name__ == '__main__':
    enviroment = getenv('ENVIRONMENT', 'development')
    app.run(
        host = '0.0.0.0', 
        port = 8090, 
        debug = (enviroment == 'development'),
        routes = routes
    )