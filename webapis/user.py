from bottle import request, response
from bottle import post, put, get
from user.view import UserView
from utils.middlewares import authenticate
from utils.errors import Error
import json
from utils.savefile import savefile


@put('/users')
@authenticate
def update_user(user = None):
    try:
        login = user.to_json().get('login')
        data = json.loads(request.body.read())

        if data.get('token'):
            token = data.get('token')
            return UserView(login).push_token(token)
        if data.get('location'):
            location = data.get('location')
            return UserView(login).update_location(location)
        if data.get('img_url'):
            return UserView(login).change_avatar(data)

        pwd = data.get('password')
        new_pwd = data.get('new_password')
        if not pwd or not new_pwd:
            return Error('passwords empty empty', 400).get_error()
        return UserView(login).change_password(pwd, new_pwd)

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
        token = data.get('token')

        if token:
            return UserView().authenticate_by_token(token)

        if not login or not password:
            return Error('Login or Password empty', 400).get_error()
        return UserView(login).authenticate(password)

    except Exception as e:
        return e


@get('/users')
@authenticate
def get_users(user=None):
    try:
        if request.query.get('query'):
            return UserView().autocomplete(request.query.get('query'))
        return UserView().list()
    except Exception as e:
        print(e)


@post('/users/image')
@authenticate
def post_image(user=None):
    """
    upload the image on the server
    @param category > type text
    @param image > type file
    @header[Content-Type] : multipart/form-data
    """
    category = 'avatars'
    image = request.files.get('image')

    return savefile(image, category)
