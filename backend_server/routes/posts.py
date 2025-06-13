from flask import Blueprint

posts = Blueprint('routes', __name__, url_prefix='/posts')
