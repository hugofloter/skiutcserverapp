from db import dbskiutc_con as db
from auth_token.model import AuthToken
from utils.errors import Error
from user.view import UserView

class AuthTokenView():
    def __init__(self):
        self.con = db()

    def get(self, token):
        """
        return the auth token if exist
        """
        with self.con:
            try:
                cur = self.con.cursor(Model= AuthToken)
                sql = "SELECT * FROM auth_token WHERE token=%s";
                cur.execute(sql, (token))

                authentication = cur.fetchone()

                if authentication is None:
                    raise Error('Not logged', 403)

                authentication = authentication.to_json()
                user = UserView(authentication['login']).get()
                
                return user

            except Error as e:
                return e.get_error()

            except Exception as e:
                return e
