from datetime import timedelta, datetime
import logging
from flask import Blueprint, make_response, jsonify, json, request
from flask_pydantic import validate
from flask_bcrypt import Bcrypt
from services.redis import session_storage
from services.schema_validation import LoginSchema, RegisterSchema, SendResetTokenSchema, ResetPasswordSchema, UserToken
from services.db import UserResponse, create_user, fetch_user_by_username
from secrets import choice
from os import getenv
from uuid import uuid4
import requests
from dotenv import load_dotenv
load_dotenv()

auth = Blueprint('auth', __name__, url_prefix='/auth')

logging.basicConfig(level=logging.INFO)

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

    redis_token = str(uuid4())
    json_dump = json.dumps({**retrieved_user.model_dump(exclude='password'), "created_at": datetime.now().isoformat()})
    session_storage.set(name=redis_token, value=json_dump, ex=timedelta(hours=72))

    response = make_response({
        "message": "Found user",
        "data": retrieved_user.model_dump(exclude=["password", "id"]),
        "token": redis_token
    })
    

    
    return response

@auth.post('/register')
@validate()
def register(body: RegisterSchema):
    user_exists = fetch_user_by_username(username=body.username) is not None
    if user_exists:
        return jsonify({"error": "Username already exists"}), 400
    
    hashed_password = bcrypt.generate_password_hash(body.password, 8) \
        .decode('utf-8')
    
    new_user: UserResponse | None = create_user(
        username=body.username,
        email=body.email,
        password=hashed_password
    )
    
    if new_user is None:
        raise ValueError("Failed to create user")
    
    redis_token = str(uuid4())
    json_dump = json.dumps({
        **new_user.model_dump(exclude='password')
        , "created_at": datetime.now().isoformat()
        
    })
    session_storage.set(name=redis_token, value=json_dump, ex=timedelta(hours=72))

    
    response = make_response({
        "message": "User registered successfully",
        "data": json_dump,
        "token": redis_token
    })
    try:
        requests.post(
            getenv("MAILER_URL", "") + "/send-welcome",
            json={
                "email": body.email,
            } 
        )
    except Exception as e:
        logging.error(f"Failed to send welcome email: {str(e)}")
    
    return response

def auth_middleware():
    try:
        print("Auth middleware triggered")
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token.split("Bearer ")[1]
        if not token:
            return jsonify({"error": "Missing access token, please login"}), 401
        logging.info(f"Token received: {token}")
        redis_data = session_storage.get(token)
        if not redis_data:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        user_data = UserToken.from_redis(redis_data)
        logging.info(f"User data retrieved: {user_data}")
        # validate user data
        
        if not user_data:
            return jsonify({"error": "Invalid user data"}), 401
        
        # check if the token is expired
        created_at = datetime.fromisoformat(user_data.created_at)
        if datetime.now() - created_at > timedelta(hours=72):
            return jsonify({"error": "Token expired, please login again"}), 401
        request.user = user_data  
    except Exception as e:
        return jsonify({"error": f"Token validation failed: {str(e)}"}), 401

def send_reset_token():
    ...

def reset_password():
    ...