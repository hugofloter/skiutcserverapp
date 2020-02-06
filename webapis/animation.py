from bottle import request, response
from bottle import get, post, delete
from animation.view import AnimationView
from utils.middlewares import authenticate, admin


@get('/animation')
@authenticate
def get_user_level(user=None):
    """get user level"""
    try:
        login = user.to_json().get('login')
        return {0: AnimationView(login=login).get_user_level()}

    except Exception as e:
        return e


@get('/animation/admin')
@admin
def get_user_level(user=None):
    """get top user level"""
    try:
        login = user.to_json().get('login')
        return AnimationView(login=login, admin=True).get_top_users()

    except Exception as e:
        return e


@get('/animation/<key>')
@authenticate
def update_animation(key, user=None):
    """unlock level"""
    try:
        login = user.to_json().get('login')
        return AnimationView(login=login).unlock_level(key, user)

    except Exception as e:
        return e
