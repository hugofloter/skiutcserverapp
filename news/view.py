from news.model import News
from db import dbskiutc_con as db
from utils.errors import Error
from datetime import datetime
from user.view import UserView
from notifications.view import NotificationsView
from notifications.model import NotificationMessage
from utils.mail import Mail


class NewsView():
    def __init__(self):
        self.con = db()

    """
    Return the list of news
    :return json of list of potin
    :raise Exception
    """
    def list(self):
        try:
            with self.con:
                cur = self.con.cursor(Model = News)
                sql = "SELECT * from news ORDER BY date DESC"
                cur.execute(sql)
                response = cur.fetchall()
                count = 0
                result = {}
                for value in response:
                    result[count] = value.to_json()
                    count += 1
                return result

        except Exception as e:
            print(e)
            return Error('Problem happened in query list', 400).get_error()

    """
    Return a news given an id
    :param id
    """
    def get(self, id):
        try:
            with self.con:
                cur = self.con.cursor(Model = News)
                sql = "SELECT * from news WHERE id = %s"
                cur.execute(sql, id)
                response = cur.fetchone()
                if response is None:
                    return {}

                return response.to_json()

        except Exception as e:
            print(e)
            return Error('Problem happened in query get', 400).get_error()

    """
    Create a news given datas model
    :param data
    """
    def create(self, data):
        try:
            with self.con:
                title = data.get('title')
                text = data.get('text')
                img_url = data.get('img_url')
                img_width = data.get('img_width')
                img_height = data.get('img_height')
                type = data.get('type')
                cur = self.con.cursor(Model = News)
                sql = "INSERT INTO news (title, text, img_url, img_width, img_height, date, type) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                now = datetime.now()
                now = now.strftime('%Y-%m-%d %H:%M:%S')
                cur.execute(sql, (title, text, img_url, img_width, img_height, now, type))
                self.con.commit()
                sql = "SELECT * FROM news WHERE id = (SELECT MAX(id) FROM news)"
                cur.execute(sql)
                last = cur.fetchone()
                tokens = UserView().list_tokens()
                message = NotificationMessage(data)
                NotificationsView(message, tokens).send_push_message()
                if type == 'email':
                    Mail().massive_mail_sender()

                return last.to_json()

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in news creation', 400).get_error()

    """
    Delete a news given an id
    :param id
    """
    def delete(self, id):
        try:
            with self.con:
                cur = self.con.cursor(Model = News)
                sql = "DELETE FROM news WHERE id = %s"
                cur.execute(sql, id)
                self.con.commit()

                return self.list()

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in news deletion', 400).get_error()
