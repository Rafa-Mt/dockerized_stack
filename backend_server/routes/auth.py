from datetime import timedelta, datetime
from flask import Blueprint, make_response, jsonify, json, request
from flask_pydantic import validate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, decode_token
from services.redis import session_storage
from services.schema_validation import LoginSchema, RegisterSchema, SendResetTokenSchema, ResetPasswordSchema, UserToken
from services.db import UserResponse, create_user, fetch_user_by_username
from secrets import choice
from string import ascii_letters, digits
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

    redis_token = str.join("", [choice(ascii_letters + digits) for _ in range(64)])
    json_dump = json.dumps({**retrieved_user.model_dump(exclude='password')})
    session_storage.set(name=redis_token, value=json_dump, ex=timedelta(hours=72))

    enconded_jwt = create_access_token(identity=str(redis_token), expires_delta=timedelta(days=2))

    response = make_response({
        "message": "Found user",
        "data": retrieved_user.model_dump(exclude=["password", "id"])
    })

    response.set_cookie(
        key="access_token",
        value=enconded_jwt,
        httponly=True,
        secure=True,
        samesite="Strict"
    )
    return response

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

def auth_middleware():
    try:
        token = request.cookies.get("access_token")
        if not token:
            return jsonify({"error": "Missing access token, please login"}), 401
        decoded_token = decode_token(token)["sub"]

        redis_token = session_storage.get(decoded_token)
        if not redis_token:
            return jsonify({"error": "Invalid or expired token"}), 401

        user_data = UserToken.from_redis(redis_token)
        request.user = user_data  
    except Exception as e:
        return jsonify({"error": f"Token validation failed: {str(e)}"}), 401

def send_reset_token():
    ...

def reset_password():
    ...