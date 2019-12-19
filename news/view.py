from news.model import News
from db import dbskiutc_con as db
from utils.errors import Error

class NewsView():
    def __init__(self):
        self.con = db()

    def list(self):
        try:
            with self.con:
                cur = self.con.cursor(Model = News)
                sql = "SELECT * from news ORDER BY date DESC";
                cur.execute(sql)

                response = cur.fetchall()

                count = 0
                result = {}
                for value in response:
                    result[count] = value.to_json()
                    count +=1;
                return result
                
        except Exception as e:
            return e
