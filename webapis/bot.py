import json

from bottle import request, response, static_file
from bottle import post, get
from utils.errors import Error
from bot.view import BotView
from utils.middlewares import admin
from config import STATIC_FILES_SOURCE

@post('/webhook')
def messenger_post_message():
    try:
        payload = request.body.read()
        signature = request.headers.get('X-Hub-Signature')

        if not payload or not signature:
             return Error('Bad request', 400).get_error()

        return BotView().validate_util_charge(payload, signature)
    except Exception as e:
        print(e)
        return Error('An error occured', 400).get_error()

@get('/webhook')
def verification():
    try:
        data = request.query
        verify_token = data.get('hub.verify_token')
        challenge = data.get('hub.challenge')

        if challenge is None or verify_token is None:
            return Error('No data', 400)
        return BotView().verify_token(verify_token, challenge)
    except Exception as e:
        return e

@post('/link_account')
def get_link_account():
    try:
        data = json.loads(request.body.read())
        login = data.get("login")
        password = data.get("password")
        token= data.get("token")

        user = BotView().update_user(token, login, password)
        return user
    except Exception as e:
        return e

@get('/static')
def get_verif_page():
    try:
        return static_file('index.html', root=STATIC_FILES_SOURCE)

    except Exception as e:
        print(e)
        return e

@get('/static/<path:path>')
def get_verif_page(path=None):
    try:
        return static_file(path, root=STATIC_FILES_SOURCE)

    except Exception as e:
        print(e)
        return e
