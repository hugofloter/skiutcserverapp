import json

from bottle import request, response
from bottle import get, post, delete
from potin.view import PotinView
from utils.middlewares import authenticate, admin


@get('/v1/potins')
@authenticate
def get_news(user=None):
    """get all potins"""
    try:
        return PotinView().list()
    except Exception as e:
        return e;


@get('/v1/potins/<id>')
@authenticate
def get_one_news(id, user=None):
    """get only one potin"""
    try:
        return PotinView().get(id)
    except Exception as e:
        return e

@post('/v1/news')
@authenticate
def create_news(user = None):
    """create a potin"""
    try:
        data = json.loads(request.body.read())
        data["approved"] = False
        return PotinView().create(data)
    except Exception as e:
        print(e)
        return e

@delete('/v1/news/<id>')
@admin
def delete_news(id, user=None):
    """delete a potin"""
    try:
        return PotinView().delete(id)
    except Exception as e:
        return e
