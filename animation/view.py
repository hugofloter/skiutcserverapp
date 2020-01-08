from animation.model import AnimationUser
from user.view import UserView
from db import dbskiutc_con as db
from utils.errors import Error


"""
Animation pist game/////
LEVEL_MAX = 11
START = 0
"""
class AnimationView():
    def __init__(self, login, admin=False):
        self.login = login
        if admin:
            self.admin=True
        else:
            self.admin=False
        self.con = db()

    """
    get current level of user
    """
    def get_user_level(self):
        try:
            with self.con:
                cur = self.con.cursor(Model=AnimationUser)
                sql = "SELECT * from `piste_anim` WHERE login_user = %s"
                cur.execute(sql, self.login)
                response = cur.fetchone()
                if response is None:
                    return {}

                return response.to_json()

        except Exception as e:
            print(e)
            return Error('Problem happened in query get', 400).get_error()

    """
    returns top ten users   
    """
    def get_top_users(self):
        if not self.admin:
            return Error('Not admin', 403).get_error()
        result = {}
        count = 0
        try:
            cur = self.con.cursor(Model=AnimationUser)
            sql = "SELECT * from `piste_anim` ORDER BY levels DESC LIMIT 10"
            cur.execute(sql)
            response = cur.fetchall()
            if response is None:
                return {}
            for u in response:
                current = u.to_json()
                result[count] = current
                count += 1
            return result

        except Exception as e:
            print(e)
            return Error('Problem happened in query get', 400).get_error()

    """
    Unlock new level
    """
    def unlock_level(self,data):


        return {}
