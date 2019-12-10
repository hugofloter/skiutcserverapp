from bottle import request, response
from bottle import post
from user.user import User
import json

@post('/users')
def create_user():
    """create a user"""
    try:
        data = json.loads(request.body.read())

        return User().reset_password('qrichard')

    except Exception as e:
        return e

@post('/authenticate')
def authenticate():
    """authenticate user"""
    try:
        data = json.loads(request.body.read())

        login = data.get('login')
        password = data.get('password')
        return User().authenticate(login, password)

    except Exception as e:
        return e
