from bottle import request
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

        return f(user=user, *args, **kwargs)

    return wrapper
