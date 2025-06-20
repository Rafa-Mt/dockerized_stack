from flask import Blueprint, request
from flask_pydantic import validate
from routes.auth import auth_middleware
from services.schema_validation import SubmitPostSchema, UserToken
from services.db import create_post, fetch_all_posts, fetch_posts_by_user

posts = Blueprint('routes', __name__, url_prefix='/posts')

@posts.before_request
def auth_wrapper():
    if request.method in ['POST', 'PUT', 'DELETE', 'GET']:
        return auth_middleware()

@posts.post("/")
@validate()
def submit_post(body: SubmitPostSchema):
    user: UserToken = request.user

    created_post = create_post(
        author_id=user.id,
        title=body.title,
        content=body.content
    )

    return {
        "message": "Created post",
        "data": created_post.model_dump()
    }

@posts.get("/")
@validate()
def get_all_posts():
    print("Fetching all posts")
    posts = fetch_all_posts()

    return {
        "message": "Found all posts",
        "data": [post.model_dump() for post in posts]
    }

@posts.get("/<username>")
@validate()
def get_posts_by_user(username: str):
    posts = fetch_posts_by_user(username=username)

    if len(posts) == 0:
        return {
            "message": "Posts not found",
            "data": None
        }, 404

    return {
        "message": "Found post",
        "data": [post.model_dump() for post in posts]
    }