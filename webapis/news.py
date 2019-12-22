import json
from bottle import request, response
from bottle import get, post, delete
from news.view import NewsView
from utils.middlewares import authenticate, admin


@get('/news')
@authenticate
def get_news(user=None):
    """get all news"""
    try:
        return NewsView().list()
    except Exception as e:
        return e


@get('/news/<id>')
@authenticate
def get_one_news(id, user=None):
    """get only one new"""
    try:
        return NewsView().get(id)
    except Exception as e:
        return e


@post('/news')
@admin
def create_news(user = None):
    """create a news"""
    try:
        data = json.loads(request.body.read())

        return NewsView().create(data)
    except Exception as e:
        print(e)
        return e


@delete('/news/<id>')
@admin
def delete_news(id, user=None):
    """delete a news"""
    try:
        return NewsView().delete(id)
    except Exception as e:
        return e
