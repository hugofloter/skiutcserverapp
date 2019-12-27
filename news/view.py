from news.model import News
from db import dbskiutc_con as db
from utils.errors import Error
from datetime import datetime


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
            return e

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
            return e

    """
    Create a news given datas model
    :param data
    """
    def create(self, data):
        try:
            with self.con:
                title = data.get('title')
                text = data.get('text')
                photo = data.get('photo')
                type = data.get('type')
                cur = self.con.cursor(Model = News)
                sql = "INSERT INTO news (title, text, photo, date, type) VALUES (%s, %s, %s, %s, %s)"
                now = datetime.now()
                now = now.strftime('%Y-%m-%d %H:%M:%S')
                cur.execute(sql, (title, text, photo, now, type))
                self.con.commit()
                sql = "SELECT * FROM news WHERE id = (SELECT MAX(id) FROM news)"
                cur.execute(sql)
                last = cur.fetchone()

                return last.to_json()

        except Exception as e:
            print(e)
            self.con.rollback()
            return e

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
            self.con.rollback()
            return e
