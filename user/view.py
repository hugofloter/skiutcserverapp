import requests
import string
import random
import secrets
from db import dbskiutc_con as db
from bottle import response
from config import SALT
from utils.errors import Error
from utils.mail import Mail
from user.model import User, Location
from urllib.parse import unquote


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
                email = self.get(self.login).to_json().get('email')
                msg = """
                Salut, participant.e à l'édition 2020 de SKI'UTC. Comme tu as pu le constater, cette année, <br>
                De la nouveauté cette année : une application SKI'UTC rien que pour toi, rien que pour vous ! <br>
                <br>
                Cours l'installer sur le store de ton téléphone (recherches SKI'UTC) <br>
                <br>
                Pour te connecter c'est simple : tu utilises ton login (ou email si tu es tremplin), et tu utilises ces codes :
                <br><br>
                <B>IDENTIFIANT : {}</B><br>
                <B>PASSWORD : {}</B><br>
                """.format(self.login, new_pwd)
                Mail().mail_sender(email, "Ton mot de passe pour l'application SKI'UTC", msg)
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
                sql = "SELECT login, lastname, firstname, email, password, isAdmin, ST_X(lastPosition) AS latitude, " \
                      "ST_Y(lastPosition) AS longitude, push_token, img_url, img_width, img_height FROM users_app WHERE login=%s and password=aes_encrypt(%s, %s)"
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
                sql = "SELECT login, lastname, firstname, email, password, isAdmin, ST_X(lastPosition) AS latitude, " \
                      "ST_Y(lastPosition) AS longitude, push_token, img_url, img_width, img_height FROM users_app WHERE login=%s"
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
                sql = "SELECT login, lastname, firstname, email, password, isAdmin, ST_X(lastPosition) AS latitude, " \
                      "ST_Y(lastPosition) as longitude, push_token, img_url, img_width, img_height FROM users_app WHERE login=%s and password=aes_encrypt(%s, %s)"
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

                    json_user = user.to_json()
                    json_user['push_token'] = user.get_push_token()
                    return {'user': json_user, 'token': token}

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

    def authenticate_by_token(self, token):
        """
        check the token to find the connected user
        """
        try:
            with self.con:
                cur = self.con.cursor(Model=User)
                sql = "SELECT users_app.login, lastname, firstname, email, password, isAdmin, ST_X(lastPosition) AS latitude, " \
                      "ST_Y(lastPosition) AS longitude, push_token, img_url, img_width, img_height FROM users_app INNER JOIN auth_token ON users_app.login=auth_token.login and auth_token.token=%s"
                cur.execute(sql,token)
                user = cur.fetchone()

                if user is None:
                    raise Error('Authentication error', 400)
                json_user = user.to_json()
                json_user['push_token'] = user.get_push_token()

                return {'user': json_user, 'token': token}

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Authentication error', 400).get_error()

    def bot_account_verification(self, pwd):
        """
        check the login and pwd given to authenticate user
        save en give a token
        """
        try:
            with self.con:
                cur = self.con.cursor(Model = User)
                sql = "SELECT login, lastname, firstname, password FROM users_app WHERE login=%s and password=aes_encrypt(%s, %s)"
                cur.execute(sql, (self.login, pwd, SALT))
                user = cur.fetchone()

                if user is None:
                    return None
                return user.to_json()

        except Error as e:
            return e.get_error()

        except Exception as e:
            print(e)
            response.status = 400
            return Error('Authentication error').get_error()

        finally:
            cur.close()
            self.con.close()

    def change_avatar(self, data):
        try:
            with self.con:
                img_url = data.get('img_url')
                img_width = data.get('img_width')
                img_height = data.get('img_height')
                cur = self.con.cursor(Model=User)
                sql = "UPDATE users_app SET img_url=%s, img_width=%s, img_height=%s WHERE login=%s"
                cur.execute(sql, (img_url, img_width, img_height, self.login))
                self.con.commit()
                return self.get(self.login).to_json()

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in changing avatar', 400).get_error()

    def get(self, login=None):
        if login is None:
            login = self.login
        with self.con:
            try:
                cur = self.con.cursor(Model= User)
                sql = "SELECT login, lastname, firstname, email, password, isAdmin, ST_X(lastPosition) as latitude, " \
                      "ST_Y(lastPosition) as longitude, push_token, img_url, img_width, img_height FROM users_app WHERE login=%s"
                cur.execute(sql, login)
                user = cur.fetchone()

                return user

            except Exception as e:
                print(e)
                return Error('Problem happened in query get', 400).get_error()

    def list(self, list=None, mail=None):
        with self.con:
            try:
                cur = self.con.cursor(Model = User)
                if list is not None:
                    t = tuple(list)
                    lookup = f"IN {t}" if len(t) > 1 else f"='{t[0]}'"
                    sql = "Select login, lastname, firstname, email, password, isAdmin, ST_X(lastPosition) AS latitude, " \
                          f"ST_Y(lastPosition) AS longitude, push_token, img_url, img_width, img_height from users_app WHERE login {lookup}"
                else:
                    sql = "Select login, lastname, firstname, email, password, isAdmin, ST_X(lastPosition) AS latitude, " \
                          "ST_Y(lastPosition) AS longitude, push_token, img_url, img_width, img_height from users_app"
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

    """
    get location of user
    :param login
    """
    def get_location(self):
        try:
            with self.con:
                cur = self.con.cursor()
                sql = "SELECT ST_X(lastPosition), ST_Y(lastPosition) FROM `users_app` WHERE login = %s"
                cur.execute(sql, self.login)
                (x, y) = cur.fetchone()
                if not x or not y:
                    return None
                location = Location({'latitude': x, 'longitude': y})

                return location.to_json()

        except Exception as e:
            print(e)
            return Error('Problem happened in query get', 400).get_error()

    """
    Update location
    :param latitude
    : param longitude
    """
    def update_location(self, location):
        try:
            latitude = location.get('latitude')
            longitude = location.get('longitude')
            with self.con:
                cur = self.con.cursor(Model=User)
                sql = "UPDATE `users_app` SET `lastPosition`= POINT(%s, %s) WHERE login = %s"
                cur.execute(sql, (latitude, longitude, self.login))
                self.con.commit()

                return self.get().to_json()
        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in updating location for user', 400).get_error()

    def push_token(self, push_token):
        try:
            with self.con:
                try:
                    cur = self.con.cursor(Model=User)
                    sql = "UPDATE users_app SET `push_token`=%s WHERE login=%s"
                    cur.execute(sql, (push_token, self.login))
                    self.con.commit()

                except Exception as e:
                    self.con.rollback()
                    raise e

                sql = "SELECT login, lastname, firstname, email, password, isAdmin, ST_X(lastPosition) AS latitude, " \
                      "ST_Y(lastPosition) as longitude, push_token, img_url, img_width, img_height FROM users_app WHERE login=%s"
                cur.execute(sql, self.login)
                user = cur.fetchone()

                return user.to_json()

        except Error as e:
            return e.get_error()

        except Exception as e:
            response.status = 501
            return Error('Problem happened in adding push token', 501).get_error()

        finally:
            self.con.close()

    def list_mail(self):
        with self.con:
            try:
                cur = self.con.cursor(Model = User)
                sql = "SELECT email FROM users_app"
                cur.execute(sql)
                user_list = cur.fetchall()
                list_mail = []
                for user in user_list:
                    list_mail.append(user.to_json().get('email'))

                return list_mail

            except Exception as e:
                response.status = 400
                return Error('Problem happened in query list', 501).get_error()

    def list_tokens(self):
        with self.con:
            try:
                cur = self.con.cursor(Model = User)
                sql = "SELECT login, push_token FROM users_app WHERE push_token IS NOT NULL"
                cur.execute(sql)
                user_list = cur.fetchall()
                list_tokens = []
                for user in user_list:
                    list_tokens.append(user.get_push_token())
                return list_tokens

            except Exception as e:
                response.status = 400
                return Error('Problem happened in query list', 501).get_error()

    def list_tokens_from_logins(self, login_list):
        with self.con:
            try:
                cur = self.con.cursor(Model = User)
                t = tuple(login_list)
                lookup = f"IN {t}" if len(t) > 1 else f"='{t[0]}'"
                sql = f"SELECT login, push_token FROM users_app WHERE push_token IS NOT NULL AND login {lookup}"
                cur.execute(sql)
                list_users = cur.fetchall()

                list_tokens = []
                for user in list_users:
                    list_tokens.append(user.get_push_token())

                return list_tokens

            except Exception as e:
                print(e)
                response.status = 400
                return Error('Problem happened in query list', 501).get_error()

    def autocomplete(self, query):
        try:
            with self.con:
                decoded_query = unquote(query)
                decoded_query = decoded_query.split(' ')
                words = []
                for word in decoded_query:
                    if len(word):
                        words.append(word)

                if not len(words):
                    return {}
                words = '|'.join(words)

                cur = self.con.cursor(Model= User)
                sql = "SELECT login, firstname, lastname, img_url, img_width, img_height FROM users_app WHERE login REGEXP %s  OR firstname REGEXP %s OR lastname REGEXP%s LIMIT 5"
                cur.execute(sql, (words, words,words))
                list_users = cur.fetchall()

                print(list_users)
                result = {}
                count = 0
                for user in list_users:
                    result[count] = user.to_json()
                    count +=1

                return result

        except Exception as e:
            print(e)
            response.status = 400
            return Error('Problem happened in query list', 501).get_error()
