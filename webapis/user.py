from bottle import request, response
from bottle import post, put, get
from user.user import User
from utils.middlewares import authenticate
import json

@put('/users')
@authenticate
def change_password(user = None):
    """change password user"""
    try:
        data = json.loads(request.body.read())
        pwd = data.get('password')
        new_pwd = data.get('new_password')

        return User(user.get_info()['login']).change_password(pwd, new_pwd)
    except Exception as e:
        print(e)
        return e

@post('/authenticate')
def authentication():
    """authenticate user"""
    try:
        data = json.loads(request.body.read())

        login = data.get('login')
        password = data.get('password')
        return User(login).authenticate(password)

    except Exception as e:
        return e


@get('/users')
@authenticate
def get_users(user=None):
    return user.list_users()
