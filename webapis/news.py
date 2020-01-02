import json
import os
import string
import random

from bottle import request, response
from bottle import get, post, delete
from news.view import NewsView
from utils.middlewares import authenticate, admin
from config import IMAGES_SOURCE
from utils.errors import Error
from utils.savefile import savefile


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

@post('/news/image')
@admin
def post_image(user=None):
    """
    upload the image on the server
    @param category > type text
    @param image > type file
    @header[Content-Type] : multipart/form-data
    """
    category = 'news'
    image = request.files.get('image')

    return savefile(image, category)


@post('/news')
@admin
def create_news(user = None):
    """create a news"""
    try:
        data = json.loads(request.body.read())
        if not data.get('title') or not data.get('text'):
            return Error('Title or text empty', 400).get_error()
        return NewsView().create(data)
    except Exception as e:
        return e


@delete('/news/<id>')
@admin
def delete_news(id, user=None):
    """delete a news"""
    try:
        return NewsView().delete(id)
    except Exception as e:
        return e
