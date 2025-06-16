from typing import Optional, Annotated
from pydantic import BaseModel, BeforeValidator, ValidationError as PydanticError
from flask import jsonify
import re

class ValidatorError(Exception):
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(message)

    def __str__(self):
        if self.field:
            return f"ValidationError in field '{self.field}': {self.message}"
        return f"ValidationError: {self.message}"

def validate_username(value: str) -> str:
    length = len(value)
    if length < 3:
        raise ValidatorError("Username must be at least 3 characters long.", "username")
    if length > 20:
        raise ValidatorError("Username must not exceed 20 characters.", "username")
    if not all(char.isalnum() or char == '_' for char in value):
        raise ValidatorError("Username must only contain alphanumeric characters or underscores.", "username")
    return value

def validate_password(value: str) -> str:
    length = len(value)
    if length < 8:
        raise ValidatorError("Password must be at least 8 characters long.", "password")
    if length > 25:
        raise ValidatorError("Password must not exceed 25 characters.", "password")
    allowed_special_chars = "!#@$%.*_"
    if not all(char.isalnum() or char in allowed_special_chars for char in value):
        raise ValidatorError(f"Password must only contain alphanumeric characters or the following special characters: {allowed_special_chars}", "password")
    return value

def validate_email(value: str) -> str:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, value):
        raise ValidatorError("Invalid email format.", "email")
    return value

def validate_token(value: str) -> str:
    if not re.fullmatch(r'[0-9a-fA-F]{6}', value):
        raise ValidatorError("Token must be a 6-character hexadecimal string.", "token")
    return value

def validate_post_title(value: str) -> str:
    if len(value) == 0:
        raise ValidatorError("Post title cannot be empty.", "title")
    if len(value) > 100:
        raise ValidatorError("Post title must not exceed 100 characters.", "title")
    return value

def validate_post_content(value: str) -> str:
    if len(value) == 0:
        raise ValidatorError("Post content cannot be empty.", "title")
    if len(value) > 500:
        raise ValidatorError("Post content must not exceed 100 characters.", "title")
    return value

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

def validation_handler(error: ValidatorError):
    return jsonify({
        "error": "validation error",
        "message": str(error.message),
        "field": str(error.field)
    }), 400

def custom_error_handler(error: Exception):
    return jsonify({
        "error": type(error).__name__,
        "message": str(error)
    }), 500