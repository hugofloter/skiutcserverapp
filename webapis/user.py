from bottle import request, response
from bottle import post, put
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

@put('/users')
def change_password():
    """change password user"""
    try:
        data = json.loads(request.body.read())
        login = data.get('login')
        pwd = data.get('password')
        new_pwd = data.get('new_password')

        return User().change_password(login, pwd, new_pwd)
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
