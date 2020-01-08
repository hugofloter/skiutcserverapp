import json
from bottle import request, response
from bottle import get, post, delete, put
from group.view import GroupView
from utils.middlewares import authenticate, admin
from user.model import Location
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
        if not data.get('name'):
            return Error('Please provide a name', 400)
        name = data.get('name')
        owner = user.to_json().get('login')
        list_login = data.get('list_login')
        return GroupView().create(name, owner, list_login)

    except Exception as e:
        return e


@get('/groups/<id>')
@authenticate
def get_group_infos(id, user=None):
    """get group and list users from id group"""
    try:
        return GroupView().get(id)

    except Exception as e:
        return e


@delete('/groups/<id>')
@authenticate
def delete_group(id, user=None):
    """deletes a group if owner"""
    try:
        data = json.loads(request.body.read())
        login = user.to_json().get('login')
        if data.get('invitation'):
            invitation_type = data.get('invitation')
            return GroupView().handle_invitation(id, login, invitation_type)
        if data.get('delete'):
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
            invitation_type = data.get('invitation')
            return GroupView().handle_invitation(id, login, invitation_type)
        if data.get('beer_call'):
            return GroupView().new_beer_call(id)
        if data.get('location_permission'):
            permission = bool(data.get('location_permission'))
            return GroupView().update_permission_location(id, login, permission)
        if data.get('list_login'):
            #send invitations
            login_list = data.get('list_login')
            GroupView().add_to_group(id, login_list=login_list)
            return GroupView().get(id)
    except Exception as e:
        return e
