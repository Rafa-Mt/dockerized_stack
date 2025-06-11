from flask import Blueprint
from flask import jsonify
from main import redis

routes = Blueprint('routes', __name__)

@routes.get('/')
def hello_world():
    value = redis.hgetall("object_test")
    return {'message': 'Hello, World!', 'value': value}

@routes.get('/test-db')
def test_db():
    try:
        redis.ping()
        return jsonify({'redis': 'connected'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500