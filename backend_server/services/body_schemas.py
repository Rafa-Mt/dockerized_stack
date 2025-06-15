from typing import Optional, Annotated
from pydantic import BaseModel, BeforeValidator
import re

def validate_username(value: str) -> str:
    length = len(value)
    if length < 3:
        raise ValueError("Username must be at least 3 characters long.")
    if length > 20:
        raise ValueError("Username must not exceed 20 characters.")
    if not all(char.isalnum() or char == '_' for char in value):
        raise ValueError("Username must only contain alphanumeric characters or underscores.")

def validate_password(value: str) -> str:
    length = len(value)
    if length < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if length > 25:
        raise ValueError("Password must not exceed 25 characters.")
    allowed_special_chars = "!#@$%.*_"
    if not all(char.isalnum() or char in allowed_special_chars for char in value):
        raise ValueError(f"Password must only contain alphanumeric characters or the following special characters: {allowed_special_chars}")
    return value

def validate_email(value: str) -> str:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, value):
        raise ValueError("Invalid email format.")
    return value

def validate_token(value: str) -> str:
    if not re.fullmatch(r'[0-9a-fA-F]{6}', value):
        raise ValueError("Token must be a 6-character hexadecimal string.")
    return value

def validate_post_title(value: str) -> str:
    ...

def validate_post_content(value: str) -> str:
    ...

Username = Annotated[str, BeforeValidator(validate_username)]
Password = Annotated[str, BeforeValidator(validate_password)]
Email = Annotated[str, BeforeValidator(validate_email)]
Token = Annotated[str, BeforeValidator(validate_token)]
PostTitle = Annotated[str, BeforeValidator(validate_post_title)]
PostContent = Annotated[str, BeforeValidator(validate_post_content)]

class LoginSchema(BaseModel):
    username: Username
    password: Password

class RegisterSchema(BaseModel):
    username: Username
    password: Password
    email: Email

class SendResetTokenSchema(BaseModel):
    email: Email

class ResetPasswordSchema(BaseModel):
    email: Email
    token: Token
    newPassword: Password

class SendPostSchema(BaseModel):
    title: PostTitle
    content: PostContent

