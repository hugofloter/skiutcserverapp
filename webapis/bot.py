import json

from bottle import request, response
from bottle import post, get
from utils.errors import Error
from bot.view import BotView
from utils.middlewares import admin

@post('/webhook')
def messenger_post_message():
    try:
        data = json.loads(request.body.read())
        print(data)
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
