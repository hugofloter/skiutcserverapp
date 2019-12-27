import json
import os
from bottle import request, response
from bottle import get, post, delete
from news.view import NewsView
from utils.middlewares import authenticate, admin

from config import IMAGES_SOURCE

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
    category = request.forms.get('category')
    image = request.files.get('image')

    name, ext = os.path.splitext(image.filename)

    if ext not in ('.png', '.jpg', '.jpeg'):
        response.status = 400
        return { "Error": "File extension not allowed." }

    save_path = f"{IMAGES_SOURCE}/{category}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = f"{save_path}/{image.filename}"
    image.save(file_path)

    return { 'img_url': file_path }


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
