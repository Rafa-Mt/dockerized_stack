from flask import Blueprint, request
from flask_pydantic import validate
from flask_bcrypt import Bcrypt
from services.redis import session_storage
from services.schema_validation import LoginSchema, RegisterSchema, SendResetTokenSchema, ResetPasswordSchema
from services.db import UserResponse, create_user, fetch_user_by_username

auth = Blueprint('auth', __name__, url_prefix='/auth')

bcrypt = Bcrypt()

@auth.post("/login")
@validate()
def login(body: LoginSchema):
    retrieved_user: UserResponse = fetch_user_by_username(username=body.username)
    if retrieved_user is None:
        raise KeyError("User does not exist")
    
    return {
        "message": "Found user",
        "data": retrieved_user.model_dump(exclude=["password",  "id"])
    }

@auth.post('/register')
@validate()
def register(body: RegisterSchema):
    user_exists = fetch_user_by_username(username=body.username) is not None
    if user_exists:
        raise ValueError("User already exist")
    
    hashed_password = bcrypt.generate_password_hash(body.password, 8) \
        .decode('utf-8')
    
    create_user(
        username=body.username,
        email=body.email,
        password=hashed_password
    )

    return {
        "message": "User created successfully"
    }

def send_reset_token():
    ...

def reset_password():
    ...