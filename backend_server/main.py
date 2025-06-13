from flask import Flask
from dotenv import load_dotenv
from os import getenv
from routes.auth import auth
from routes.posts import posts

load_dotenv()  

app = Flask(__name__)

if __name__ == '__main__':
    enviroment = getenv('ENVIRONMENT', 'development')
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.run(
        host = '0.0.0.0', 
        port = 8090, 
        debug = (enviroment == 'development'),
    )