import string
import random

from config import WEBHOOK_TOKEN
from db import dbskiutc_con as db
from utils.errors import Error

class BotView():
    def __init__(self):
        self.con = db()

    def verify_token(self, token, challenge):
        try:
            if token == WEBHOOK_TOKEN:
                return challenge
            raise Error("Bad token.", 400)

        except Exception as e:
            print(e)
            return e.get_error()
