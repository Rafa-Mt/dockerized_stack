from flask import Blueprint, request, jsonify
from services.redis import session_storage

auth = Blueprint('auth', __name__, url_prefix='/auth')
@auth.post("/redis")
def load_to_redis():
    body = request.get_json()
    print(body)
    return body

@auth.get('/')
def hello_world():
    value = session_storage.hgetall("object_test")
    return {'message': 'Hello, World!', 'value': value}
