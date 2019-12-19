from bottle import request
from utils.errors import Error
from db import dbskiutc_con as db
from auth_token.view import AuthTokenView
from functools import wraps

def authenticate(f):
    """
    :param f: every api rest functions
    :return: function if user is auth
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if auth is None:
            return Error('Not Logged', 403).get_error()
        user = AuthTokenView().get(auth)

        if isinstance(user, dict):
            return user
        return f(user=user, *args, **kwargs)

    return wrapper


def admin(f):
    """
    :param f: every api rest functions
    :return: function if user is auth
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if auth is None:
            return Error('Not Logged', 403).get_error()
        user = AuthTokenView().get(auth)

        if isinstance(user, dict):
            return user

        if not user.to_json()['isAdmin']:
            return Error('Not Admin', 403).get_error()

        return f(user=user, *args, **kwargs)

    return wrapper
