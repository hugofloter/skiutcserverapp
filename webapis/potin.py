import json

from bottle import request, response
from bottle import get, post, delete, put
from potin.view import PotinView
from utils.middlewares import authenticate, admin


@get('/potins')
@authenticate
def get_potins(user=None):
    """get all potins"""
    try:
        return PotinView().list()
    except Exception as e:
        return e;


@get('/potins/<id>')
@authenticate
def get_one_potin(id, user=None):
    """get only one potin"""
    try:
        return PotinView().get(id)
    except Exception as e:
        return e


@post('/potins')
@authenticate
def create_potin(user = None):
    """create a potin"""
    try:
        data = json.loads(request.body.read())
        data["approved"] = False
        data["sender"] = user.to_json().get("login")

        return PotinView().create(data)

    except Exception as e:
        print(e)
        return e

@delete('/potins/<id>')
@admin
def delete_potin(id, user=None):
    """delete a potin"""
    try:
        return PotinView().delete(id)
    except Exception as e:
        return e


@get('/potins/admin')
@admin
def get_unapproved_potin(user=None):
    """get list of potin not approved yet"""
    try:
        return PotinView().list(admin = True)
    except Exception as e:
        return e


@put('/potins/<id>')
@admin
def update_potin(id, user=None):
    """update a potin and set to approved"""
    try:
        return PotinView().update(id)
    except Exception as e:
        return e
