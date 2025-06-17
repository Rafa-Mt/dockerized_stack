from flask import Blueprint, request
from flask_pydantic import validate
from routes.auth import auth_middleware
from services.schema_validation import SubmitPostSchema

posts = Blueprint('routes', __name__, url_prefix='/posts')

@posts.before_request
def auth_wrapper():
    return auth_middleware()

@posts.post("/")
@validate()
def submit_post(body: SubmitPostSchema):
    return {
        "user": request.user,
        "body": body.model_dump()
    }