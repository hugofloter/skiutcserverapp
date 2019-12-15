import requests
import string
import random
import secrets
from db import dbskiutc_con as db
from bottle import response
from config import SKIUTC_SERVICE, GINGER_URL, GINGER_KEY, SALT
from utils.errors import Error
import json

class User():
    def __init__(self, login):
        try:
            con = db()
            with con:
                cur = con.cursor()
                sql = "SELECT * FROM users_app WHERE login = %s";
                cur.execute(sql, (login))

                self.user = cur.fetchone()

                if self.user is None:
                    raise Error('Not Found', 404)
        except Exception as e:
            return

    def get_info(self):
        user = self.user
        del user['password']
        return user

    def reset_password(self):
        """
        generate a new password for the login and send it by mail
        """
        letters = string.ascii_lowercase
        new_pwd = ''.join(random.choice(letters) for i in range(10))

        try:
            con = db()
            with con:
                cur = con.cursor()
                sql = "UPDATE users_app SET password=aes_encrypt(%s, %s) WHERE login=%s;"
                cur.execute(sql, (new_pwd, SALT, self.user['login']))
                con.commit()

                #Here we have to send the the new password to the email.
                return new_pwd

        except Exception as e:
            con.rollback()
            response.status = 401
            return { 'error': 'Change password error.' }

    def change_password(self, pwd, new_pwd):
        """
        to allow the user to change his password
        """
        try:
            con = db()
            with con:
                cur = con.cursor()
                sql = "SELECT * FROM users_app WHERE login=%s and password=aes_encrypt(%s, %s)";
                cur.execute(sql, (self.user['login'], pwd, SALT))

                user = cur.fetchone()
                if user is None:
                    raise Error('Not found', 404)
                try:
                    sql = "UPDATE users_app SET password=aes_encrypt(%s, %s) WHERE login=%s;"
                    cur.execute(sql, (new_pwd, SALT, self.user['login']))
                    con.commit()
                except Exception as e:
                    raise e
                    con.rollback()

                return self.get_info()

        except Error as e:
            return e.get_error()

        except Exception as e:
            print(e)
            response.status =  501
            return e
        finally:
            con.close()

    def authenticate(self, pwd):
        """
        check the login and pwd given to authenticate user
        save en give a token
        """

        try:
            con = db()
            with con:
                cur = con.cursor()
                sql = "SELECT * FROM users_app WHERE login=%s and password=aes_encrypt(%s, %s)";
                cur.execute(sql, (self.user['login'], pwd, SALT))

                user = cur.fetchone()

                if user is None:
                    raise Error('Authentication error', 403)

                token = secrets.token_hex(25)
                try:
                    sql = "DELETE FROM auth_token WHERE login=%s;"
                    cur.execute(sql, (self.user['login']))

                    sql = "INSERT INTO auth_token (login, token) VALUES (%s, %s);"
                    cur.execute(sql, (self.user['login'], token))
                    con.commit()

                    return { 'user': self.get_info(), 'token': token }
                except Exception as e:
                    con.rollback()
                    raise Error('Authentication error', 403)
        except Error as e:
            return e.get_error()

        except Exception as e:
            print(e)
            response.status = 400
            return {"error": 'Bad Request'}
        finally:
            cur.close()
            con.close()


    def list_users(self):
        con = db()
        with con:
            try:
                cur = con.cursor()
                sql = "Select * from users_app";
                cur.execute(sql)

                users = cur.fetchall()

                users_dict = {}
                count = 0
                for user in users:
                    del user['password']
                    users_dict[count] = user
                    count +=1

                return users_dict
            except Exception as e:
                response.status = 400
                return { "error": 'Bad Request.' }
