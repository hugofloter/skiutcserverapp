from bottle import request
from db import dbskiutc_con as db
from utils.errors import Error
from functools import wraps
from user.user import User

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

        con = db()
        with con:
            try:
                cur = con.cursor()
                sql = "SELECT * FROM auth_token WHERE token=%s";
                cur.execute(sql, (auth))

                authentication = cur.fetchone()

                if authentication is None:
                    raise Error('Not logged', 403)

                user = User(authentication['login'])
                return f(user=user, *args, **kwargs)

            except Error as e:
                return e.get_error()

            except Exception as e:
                return e

    return wrapper
