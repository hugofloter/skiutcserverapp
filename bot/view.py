import string
import random
import hashlib
import hmac
import json
import requests

from requests_toolbelt import MultipartEncoder
from datetime import datetime
from time import strptime
from db import dbskiutc_con as db
from config import WEBHOOK_TOKEN, APP_SECRET, FB_MESSAGE_API, PAGE_TOKEN, API_URL
from bot.model import BotUser
from utils.errors import Error
from user.view import UserView

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

            payload = json.loads(payload)
            entry = payload.get('entry')

            for e in entry:
                webhook_event = e.get('messaging')[0]
                sender = webhook_event.get('sender').get('id')
                page = webhook_event.get('recipient').get('id')
                timestamp = webhook_event.get('timestamp')

                if webhook_event.get('message'):
                    self.handleMessage(sender, webhook_event.get('message'), timestamp)

            return 'EVENT_RECEIVED'
        except Exception as e:
            print(e)
            return e

    def get_user(self, sender_psid, timestamp):
        try:
            with self.con:
                cur = self.con.cursor(Model = BotUser )
                sql = "SELECT * FROM bot_users WHERE fb_id=%s"
                cur.execute(sql, sender_psid)
                user = cur.fetchone()

                time = datetime.fromtimestamp(timestamp / 1000)
                time = time.strftime('%Y-%m-%d %H:%M:%S')

                if user is None:
                    letters = string.ascii_lowercase + string.digits
                    token = ''.join(random.choice(letters) for i in range(16))

                    sql = "INSERT INTO bot_users (fb_id, last_action, token) VALUES (%s, %s, %s)"
                    cur.execute(sql, (sender_psid, time, token))
                    self.con.commit()
                    return { "token": token }

                sql = "UPDATE bot_users SET last_action=%s WHERE fb_id=%s"
                cur.execute(sql, (time, sender_psid))
                self.con.commit()

                user = user.to_json()
                user['last_action'] = time

                if user.get('login') == None:
                    return { "token": user.get('token') }

                return user

        except Exception as e:
            print(e)
            self.con.rollback()
            return e

    def get_user_by_login(self, login):
        try:
            with self.con:
                cur = self.con.cursor(Model = BotUser )
                sql = "SELECT * FROM bot_users WHERE login=%s"
                cur.execute(sql, login)
                user = cur.fetchone()

                return user

        except Exception as e:
            print(e)
            return e

    def get_random_user(self, sender_psid):
        try:
            with self.con:
                cur = self.con.cursor(Model = BotUser )

                sql = "SELECT * FROM bot_users WHERE NOT login=%s AND login IS NOT NULL ORDER BY RAND() LIMIT 1"
                cur.execute(sql, sender_psid)
                user = cur.fetchone()

                return user

        except Exception as e:
            print(e)
            return e

    def update_user(self, token, login, password):
        try:
            user = UserView(login).bot_account_verification(password)
            if user is None:
                raise Error('error Login', 400)

            with self.con:
                cur = self.con.cursor(Model = BotUser )
                sql = "UPDATE bot_users SET token=NULL, login=%s WHERE token=%s"
                cur.execute(sql, (login, token))
                self.con.commit()

                if cur.rowcount == 0:
                    raise Error('Invalid token', 400)

                user = self.get_user_by_login(login).to_json()
                response = {
                    "text": "Bien joué! Tu peux maintenant envoyer n'importe quelle photo (soit pas trop hardcore quand meme on te connait... :p ) et moi je m'occuperai de la balancer à un pote de Ski'UTC random!"
                }
                self.callSendAPI(user.get('fb_id'), response)

                return UserView(login).get().to_json()

        except Exception as e:
            self.con.rollback()
            return e.get_error()

    def handleMessage(self, sender_psid, received_message, timestamp) :

        user = self.get_user(sender_psid, timestamp)
        response = {}

        if user.get('token'):
            response = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [{
                            "title": "Lie ton compte Ski'UTC",
                            "subtitle": "Pour participer aux jeux, lie ton compte de l'appli Ski'UTC",
                            "buttons": [{
                                "type": "web_url",
                                "url": f"{API_URL}/static?token={user['token']}",
                                "webview_height_ratio": "full",
                                "messenger_extensions": "false",
                                "title": "Lier mon compte!",
                            }]
                        }]
                    }
                }
            }
            self.callSendAPI(sender_psid, response)
            return None

        if received_message.get('text'):
            answers = [
                f"Arrête avec tes '{received_message['text']}' et balance plutôt des dossiers",
                "AH BAAAAN! ON LUI DIT PHOTO ET LE MEC IL ENVOIE PAS DES PHOTOOOOS!",
                "stop spam ou je te bloque. envoie des photos si tu veux te rendre utile"
            ]
            response = {
                "text": random.choice(answers)
                }

        elif received_message.get('attachments') and len(received_message['attachments']):

            type = received_message['attachments'][0]['type']
            payload = received_message['attachments'][0]['payload']
            if type == "image":
                answers = [
                    "Wowwh une photo!! Vas y je vais la faire tourner à un de tes potes!",
                    "Oh la gueule que t'as! ca va tourner direct ça!",
                    "MDR pas mal celle là! Encore un mec qui va rien comprendre quand il la verra...",
                    "T'es sérieux? c'est ca ta photo? t'es pas influenceur sur insta toi... Bon allez je l'envoie mais hésite pas à t'améliorer"
                ]

                recipient = self.get_random_user(sender_psid).to_json().get('fb_id')
                image = payload.get('url')

                print(f"envoie de {image} a {recipient}")
                self.send_image(recipient, image)

                response = {
                    "text": random.choice(answers)
                }
            elif type == "video":
                answers = [
                    "Eh t'as cru que je voulais voir ta sex-tape? envoie plutot des photos",
                    "Tu fous quoi à balancer des vidéos?? ON VEUT DES PHOTAL",
                    "T'es bourré toi! c'est de la photo que je veux! DU CUL DU CUL DU CUL"
                ]
                response = {
                    "text": random.choice(answers)
                }
            else:
                answers = [
                    "Ptin je comprend meme pas ce que tu m'envoie comme truc!",
                    "T'es bourré toi! moi je veux des photos!!"
                ]
                response = {
                    "text": random.choice(answers)
                }

        else:
            response = {
                "text": "MDR j'ai rien compris à ce que tu voulais! t'es déjà bourré toi!"
            }
        self.callSendAPI(sender_psid, response)

    def send_image(self, recipient_psid, image_url):
        response = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url,
                    "is_reusable": "true"
                }
            }
        }

        self.callSendAPI(recipient_psid, response)

    def callSendAPI(self, sender_psid, response):
        request_body = {
            "recipient": {
                "id": sender_psid
            },
            "message": response
        }


        params =  { "access_token": PAGE_TOKEN }
        try:
            response = requests.post(FB_MESSAGE_API, json = request_body, params=params)
        except Exception as e:
            print(e)
