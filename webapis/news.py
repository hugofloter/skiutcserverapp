from bottle import request, response
from bottle import get, post, put
from news.view import NewsView
from utils.middlewares import authenticate

@get('/v1/news')
def get_news(user=None):
    """get all news"""
    try:
        view = NewsView()

        return view.list()
    except Exception as e:
        return e;
