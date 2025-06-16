from flask import Flask
from dotenv import load_dotenv
from os import getenv
from routes.auth import auth
from routes.posts import posts
from services.schema_validation import ValidatorError, validation_handler, custom_error_handler

load_dotenv()  
app = Flask(__name__)

if __name__ == '__main__':
    enviroment = getenv('ENVIRONMENT', 'development')

    @app.errorhandler(ValidatorError)
    def validator_wrapper(error):
        return validation_handler(error)
    
    @app.errorhandler(Exception)
    def exception_handler(error):
        return custom_error_handler(error)
    
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.run(
        host = '0.0.0.0', 
        port = 8090, 
        debug = (enviroment == 'development'),
    )