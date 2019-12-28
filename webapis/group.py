import json
from bottle import request, response
from bottle import get, post, delete, put
from group.view import GroupView
from utils.middlewares import authenticate, admin
from utils.errors import Error


@get('/groups')
@authenticate
def get_groups(user=None):
    """get groups from login"""
    try:
        return GroupView().list(user.to_json().get('login'))

    except Exception as e:
        return e


@post('/groups')
@authenticate
def create_group(user=None):
    """création d'un groupe"""
    try:
        data = json.loads(request.body.read())
        list_login = data.get('list_login')
        return GroupView().create(data, list_login)

    except Exception as e:
        return e


@get('/groups/<id>')
@authenticate
def get_group_infos(id, user=None):
    """get groups and list users from login"""
    try:
        return GroupView().get(id)

    except Exception as e:
        return e


@delete('/groups/<id>')
@authenticate
def delete_group(id, user=None):
    """deletes a group if owner"""
    try:
        login = user.to_json().get('login')
        return GroupView().delete(id, login)

    except Exception as e:
        return e


@put('/groups/<id>')
@authenticate
def update_group(id, user=None):
    """Update a group"""
    try:
        data = json.loads(request.body.read())
        login = user.to_json().get('login')
        if data.get('invitation'):
            return GroupView().accept_group(id, login)
        if data.get('beer_call'):
            return GroupView().new_beer_call(id)
        #@TODO Missig sharing position allow

    except Exception as e:
        return e
