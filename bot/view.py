import string
import random
import hashlib
import hmac

from config import WEBHOOK_TOKEN, APP_SECRET
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

    def validate_util_charge(self, payload, signature):
        try:
            hash = hmac.new(APP_SECRET.encode('utf-8'), payload, hashlib.sha1).hexdigest()
            if hash != signature.split('=')[-1]:
                raise Error('Not the same hash', 400)
            return None
        except Exception as e:
            print(e)
            return e
