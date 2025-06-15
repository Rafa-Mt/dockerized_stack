from flask import Blueprint, request
from flask_pydantic import validate
from services.redis import session_storage
from services.body_schemas import LoginSchema, RegisterSchema, SendResetTokenSchema, ResetPasswordSchema

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.post("/login")
@validate(body = LoginSchema)
def login(body: LoginSchema):

    print(body)
    return body

@auth.get('/register')
@validate()
def register():
    value = session_storage.hgetall("object_test")
    return {'message': 'Hello, World!', 'value': value}

def send_reset_token():
    ...

def reset_password():
    ...