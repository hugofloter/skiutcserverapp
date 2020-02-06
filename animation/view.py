from animation.model import AnimationUser, AnimationKey
from user.view import UserView
from db import dbskiutc_con as db
from utils.errors import Error
from utils.mail import Mail


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
    Update user level
    """
    def update_user_level(self, new_level):
        try:
            with self.con:
                cur = self.con.cursor(Model=AnimationUser)
                sql = "UPDATE `piste_anim` SET `level`=%s WHERE login_user = %s"
                cur.execute(sql, (new_level, self.login))
                self.con.commit()
                return self.get_user_level()

        except Exception as e:
            print(e)
            return Error('Problem happened in updating user level', 400).get_error()

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
            sql = "SELECT * from `piste_anim` ORDER BY `level` DESC LIMIT 10"
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
    def unlock_level(self, key, user):
        try:
            users_info = self.get_user_level()
            with self.con:
                cur = self.con.cursor(Model=AnimationKey)
                sql = "SELECT `level`, `next_indice` from `anim_key` WHERE `key`=%s"
                cur.execute(sql, key)
                response = cur.fetchone()
                if response is None:
                    return {}
                target_anim = response.to_json()
                if users_info.get('level') + 1 == target_anim.get('level'):
                    user_mail = user.to_json().get('email')
                    Mail().mail_sender(user_mail, "Ton nouvel indice", target_anim.get('next_indice'))
                    return self.update_user_level(target_anim.get('level'))
                else:
                    return Error('Unauthorized animation level target', 403).get_error()

        except Exception as e:
            print(e)
            return Error('Problem happened in query get', 400).get_error()
