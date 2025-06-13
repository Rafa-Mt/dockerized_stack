from flask import Flask
from dotenv import load_dotenv
from os import getenv
from services.routes import routes

load_dotenv()  

app = Flask(__name__)

if __name__ == '__main__':
    enviroment = getenv('ENVIRONMENT', 'development')
    app.register_blueprint(routes)
    app.run(
        host = '0.0.0.0', 
        port = 8090, 
        debug = (enviroment == 'development'),
    ) \
    