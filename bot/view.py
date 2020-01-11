import string
import random

from bot.model import BotTokenChallenge
from db import dbskiutc_con as db
from utils.errors import Error

class BotView():
    def __init__(self):
        self.con = db()

    def create_challenge_token(self):
        letters = string.ascii_lowercase
        numbers = "0123456789"

        try:
            token = ''.join(random.choice(letters+numbers) for i in range(30))

            with self.con:
                cur = self.con.cursor(Model = BotTokenChallenge)
                sql = "INSERT INTO bot_token_challenge (token) VALUES (%s)"
                cur.execute(sql, token)
                self.con.commit()

            return { "token": token }

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Error creating key', 400).get_error()

    def verify_token(self, token, challenge):
        try:
            with self.con:
                cur = self.con.cursor(Model = BotTokenChallenge)
                sql = "SELECT * FROM bot_token_challenge WHERE token=%s"
                cur.execute(sql, (token))

                response = cur.fetchone()

                if response is None:
                    return Error('Token does not exist', 403).get_error()

                sql = "UPDATE bot_token_challenge SET challenge=%s WHERE token=%s";
                cur.execute(sql, (challenge, token))
                self.con.commit()
                
                return {
                    'hub': {
                        'challenge': challenge
                    }
                }
        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Error verifying the token', 400).get_error()
