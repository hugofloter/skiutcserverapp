import requests
import string
import random
import secrets
from db import dbskiutc_con as db
from bottle import response
from config import SALT
from utils.errors import Error
import json

from user.model import User


class UserView():
    def __init__(self, login = None):
        self.con = db()
        self.login = login

    def reset_password(self):
        """
        generate a new password for the login and send it by mail
        """
        letters = string.ascii_lowercase
        new_pwd = ''.join(random.choice(letters) for i in range(10))

        try:
            with self.con:
                cur = self.con.cursor(Model = User)
                sql = "UPDATE users_app SET password=aes_encrypt(%s, %s) WHERE login=%s;"
                cur.execute(sql, (new_pwd, SALT, self.login))
                self.con.commit()
                #@TODO Here we have to send the the new password to the email.
                return new_pwd

        except Exception as e:
            print(e)
            self.con.rollback()
            response.status = 400
            return Error('Error happened in password reset process').get_error()

    def change_password(self, pwd, new_pwd):
        """
        to allow the user to change his password
        """
        try:
            with self.con:
                cur = self.con.cursor(Model = User)
                sql = "SELECT * FROM users_app WHERE login=%s and password=aes_encrypt(%s, %s)"
                cur.execute(sql, (self.login, pwd, SALT))
                user = cur.fetchone()
                if user is None:
                    raise Error('Not found', 404)
                try:
                    sql = "UPDATE users_app SET password=aes_encrypt(%s, %s) WHERE login=%s"
                    cur.execute(sql, (new_pwd, SALT, self.login))
                    self.con.commit()
                except Exception as e:
                    self.con.rollback()
                    raise e
                sql = "SELECT * FROM users_app WHERE login=%s"
                cur.execute(sql, self.login)
                user = cur.fetchone()

                return user.to_json()

        except Error as e:
            return e.get_error()

        except Exception as e:
            print(e)
            response.status = 400
            return Error('Error happened during password change process').get_error()

        finally:
            self.con.close()

    def authenticate(self, pwd):
        """
        check the login and pwd given to authenticate user
        save en give a token
        """
        try:
            with self.con:
                cur = self.con.cursor(Model = User)
                sql = "SELECT * FROM users_app WHERE login=%s and password=aes_encrypt(%s, %s)"
                cur.execute(sql, (self.login, pwd, SALT))
                user = cur.fetchone()
                if user is None:
                    raise Error('Authentication error', 400)
                token = secrets.token_hex(25)
                try:
                    sql = "DELETE FROM auth_token WHERE login=%s"
                    cur.execute(sql, self.login)
                    sql = "INSERT INTO auth_token (login, token) VALUES (%s, %s)"
                    cur.execute(sql, (self.login, token))
                    self.con.commit()

                    return {'user': user.to_json(), 'token': token}

                except Exception as e:
                    self.con.rollback()
                    raise Error('Authentication error', 400)

        except Error as e:
            return e.get_error()

        except Exception as e:
            print(e)
            response.status = 400
            return Error('Authentication error').get_error()

        finally:
            cur.close()
            self.con.close()

    def get(self, login=None):
        if login is None:
            login = self.login
        with self.con:
            try:
                cur = self.con.cursor(Model= User)
                sql = "SELECT * FROM users_app WHERE login=%s"
                cur.execute(sql, login)
                user = cur.fetchone()

                return user

            except Exception as e:
                print(e)
                return Error('Problem happened in query get', 400).get_error()

    def list(self):
        with self.con:
            try:
                cur = self.con.cursor(Model = User)
                sql = "Select * from users_app"
                cur.execute(sql)
                users = cur.fetchall()
                users_dict = {}
                count = 0
                for user in users:
                    users_dict[count] = user.to_json()
                    count += 1

                return users_dict

            except Exception as e:
                print(e)
                response.status = 400
                return Error('Problem happened in query list').get_error()
