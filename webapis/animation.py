from bottle import request, response
from bottle import get, post, delete
from animation.view import AnimationView
from utils.middlewares import authenticate, admin


@get('/animation')
@authenticate
def get_user_level(user=None):
    """get all news"""
    try:
        login = user.to_json().get('login')
        is_admin = user.to_json().get('isAdmin')
        if is_admin:
            return AnimationView(login=login, admin=is_admin).get_top_users()
        else:
            return AnimationView(login=login). get_user_level()

    except Exception as e:
        return e


@get('/animation/<key>')
@authenticate
def update_animation(key, user=None):
    """get all news"""
    try:
        login = user.to_json().get('login')
        return AnimationView(login=login).unlock_level(key)

    except Exception as e:
        return e
