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
        login = user.to_json().get('login')
        return GroupView(login).list(login)

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
        return GroupView(owner).create(name, owner, list_login)

    except Exception as e:
        return e


@get('/groups/<id>')
@authenticate
def get_group_infos(id, user=None):
    """get group and list users from id group"""
    try:
        login = user.to_json().get('login')
        return GroupView(login).get(id)

    except Exception as e:
        return e


@delete('/groups/<id>')
@authenticate
def delete_group(id, user=None):
    try:
        data = json.loads(request.body.read())
        login = user.to_json().get('login')
        # refuse invitation
        if data.get('invitation'):
            invitation_type = data.get('invitation')
            return GroupView(login).handle_invitation(id, login, invitation_type)
        """deletes a group if owner, leave group if member"""
        return GroupView(login).delete(id, login)

    except Exception as e:
        return e

@put('/groups/<id>')
@authenticate
def update_group(id, user=None):
    """Update group and retrieve one group"""
    try:
        data = json.loads(request.body.read())
        login = user.to_json().get('login')
        if data.get('invitation'):
            invitation_type = data.get('invitation')
            return GroupView(login).handle_invitation(id, login, invitation_type)
        if data.get('beer_call'):
            return GroupView(login).new_beer_call(id)
        if 'location_permission' in data:
            print('oui')
            permission = bool(data.get('location_permission'))
            return GroupView(login).update_permission_location(id, login, permission)
        if data.get('list_login'):
            #send invitations
            login_list = data.get('list_login')
            GroupView(login).add_to_group(id, login_list=login_list)
            return GroupView(login).get(id)
        if data.get('to_remove'):
            GroupView(login).remove_from_group(id, data.get('to_remove'), owner=login)
            return GroupView(login).get(id)
    except Exception as e:
        return e
