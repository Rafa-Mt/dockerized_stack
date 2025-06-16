from datetime import timedelta
from flask import Blueprint, make_response, jsonify
from flask_pydantic import validate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from services.redis import session_storage
from services.schema_validation import LoginSchema, RegisterSchema, SendResetTokenSchema, ResetPasswordSchema
from services.db import UserResponse, create_user, fetch_user_by_username
from secrets import token_bytes
from os import getenv

auth = Blueprint('auth', __name__, url_prefix='/auth')

bcrypt = Bcrypt()

@auth.post("/login")
@validate()
def login(body: LoginSchema):
    retrieved_user: UserResponse = fetch_user_by_username(username=body.username)
    if retrieved_user is None:
        raise KeyError("Invalid username")
    
    valid_login = bcrypt.check_password_hash(retrieved_user.password, body.password)
    if not valid_login:
        raise KeyError("Invalid password")

    redis_token = token_bytes(32) \
        .decode("utf-8")
    
    session_storage.set(redis_token, retrieved_user.model_dump(), ex=60 * 60 * 24 * 7)
    enconded_jwt = create_access_token(identity=str(redis_token), expires_delta=timedelta(days=2))
    print({"jwt": enconded_jwt, "redis-token": redis_token})
    response = make_response(jsonify({
        "message": "Found user",
        "data": retrieved_user.model_dump(exclude=["password", "id"])
    }))
    response.set_cookie(
        key="access_token",
        value=enconded_jwt,
        httponly=True,
        secure=True,
        samesite="Strict"
    )
    return jsonify(response)

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