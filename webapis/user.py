from bottle import request, response
from bottle import post, put, get
from user.view import UserView
from utils.middlewares import authenticate
import json

@put('/v1/users')
@authenticate
def change_password(user = None):
    """change password user"""
    try:
        data = json.loads(request.body.read())
        pwd = data.get('password')
        new_pwd = data.get('new_password')

        user = user.to_json()
        return UserView(user['login']).change_password(pwd, new_pwd)
    except Exception as e:
        print(e)
        return e

@post('/v1/authenticate')
def authentication():
    """authenticate user"""
    print("loginnnnnnnn")
    try:
        data = json.loads(request.body.read())

        login = data.get('login')
        password = data.get('password')
        return UserView(login).authenticate(password)

    except Exception as e:
        return e


@get('/v1/users')
@authenticate
def get_users(user=None):
    try:
        return UserView().list()
    except Exception as e:
        print(e)
