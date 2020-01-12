import string
import random
import hashlib

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

    def validate_util_charge(self, charge, signature):
        try:
            hash = hashlib.sha1(charge+ WEBHOOK_TOKEN)
            
        except Exception as e:
            print(e)
            return e
