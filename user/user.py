import requests
import string
import random
import jwt
from db import dbskiutc_con as db
from bottle import response
from config import SKIUTC_SERVICE, GINGER_URL, GINGER_KEY, SALT, TOKEN_KEY
from utils.errors import AuthenticationError
import json

class User():
    def reset_password(self, login):
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
                cur.execute(sql, (new_pwd, SALT, login))
                con.commit()

                #Here we have to send the the new password to the email.
                return new_pwd

        except Exception as e:
            con.rollback()
            response.status = 401
            return { 'error': 'Change password error.' }

    def change_password(self, login, pwd, new_pwd):
        """
        to allow the user to change his password
        """
        print("a")

    def authenticate(self, login, pwd):
        """
        check the login and pwd given to authenticate user
        save en give a token
        """

        try:
            con = db()
            with con:
                cur = con.cursor()
                sql = "SELECT * FROM users_app WHERE login=%s and password=aes_encrypt(%s, %s)";
                cur.execute(sql, (login, pwd, SALT))

                user = cur.fetchone()

                if user is None:
                    raise AuthenticationError

                del user['password']
                encoded = jwt.encode(user,TOKEN_KEY, algorithm='HS256')
                try:
                    sql = "DELETE FROM auth_token WHERE login=%s;"
                    cur.execute(sql, (login))

                    sql = "INSERT INTO auth_token (login, token) VALUES (%s, %s);"
                    cur.execute(sql, (login, encoded))
                    con.commit()

                    return { 'user': user, 'token': encoded.decode() }
                except:
                    con.rollback()
                    raise AuthenticationError
        except AuthenticationError:
            response.status = 403
            return {"error": 'Authentication error'}

        except Exception as e:
            print(e)
            response.status = 400
            return {"error": 'Bad Request'}
        finally:
            cur.close()
            con.close()
