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
from bot.model import BotUser, BotMessage
from utils.errors import Error
from user.view import UserView
from bot.utils import create_question, send_question, add_answer, answers_stats, list_question

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
                if webhook_event.get('postback'):
                    self.handle_postback(webhook_event.get('postback'), sender)
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

                sql = "SELECT * FROM bot_users WHERE login IS NOT NULL AND NOT login=%s  ORDER BY RAND() LIMIT 1"
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
                self.basic_answer(user.get('fb_id'), 'new')

                return UserView(login).get().to_json()

        except Exception as e:
            self.con.rollback()
            return e.get_error()

    def handleMessage(self, sender_psid, received_message, timestamp):

        user = self.get_user(sender_psid, timestamp)
        response = {}

        if user.get('token'):
            return self.send_invitation(user['token'], sender_psid)

        message = received_message.get('text')

        if self.parse_question(message, sender_psid):
            return

        if message and len(message) and "jouer" in message.lower():
            return self.send_question(sender_psid)

        if message and len(message) and ("stats" in message.lower() or "statistiques" in message.lower()):
            return self.send_question(sender_psid)

        if message:
            return self.basic_answer(sender_psid)

        if received_message.get('attachments') and len(received_message['attachments']):

            type = received_message['attachments'][0]['type']
            payload = received_message['attachments'][0]['payload']

            recipient = self.get_random_user(sender_psid).to_json().get('fb_id')
            url = payload.get('url')

            self.send_attachement(recipient, url, type)
            return self.basic_answer(sender_psid, 'image')
        return self.basic_answer(sender_psid, 'other')

    def send_attachement(self, recipient_psid, url, type):
        response = {
            "attachment": {
                "type": type,
                "payload": {
                    "url": url
                }
            }
        }

        self.callSendAPI(recipient_psid, response)

    def basic_answer(self, sender_psid, type='text'):
        answer = self.get_message(random=True, type=type)
        response = {
            "text": answer.get('text', 'oupsi je sais plus ce que je voulais dire')
        }
        self.callSendAPI(sender_psid, response)

    def send_invitation(self, token, sender_psid):
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
                            "url": f"{API_URL}/static?token={token}",
                            "webview_height_ratio": "full",
                            "messenger_extensions": "false",
                            "title": "Lier mon compte!",
                        }]
                    }]
                }
            }
        }
        self.callSendAPI(sender_psid, response)

    def callSendAPI(self, sender_psid, response):
        request_body = {
            "recipient": {
                "id": sender_psid
            },
            "message": response
        }
        params = { "access_token": PAGE_TOKEN }
        try:
            print(request_body)
            response = requests.post(FB_MESSAGE_API, json = request_body, params=params)
        except Exception as e:
            print(e)

    def add_message(self, text, type = 'text'):
        try:
            with self.con:
                cur = self.con.cursor(Model = BotMessage )
                sql = "INSERT INTO bot_messages (text, type) VALUES (%s, %s)"
                cur.execute(sql, (text, type))
                self.con.commit()

                sql = "SELECT * FROM bot_messages WHERE id = (SELECT MAX(id) FROM bot_messages)"
                cur.execute(sql)

                message = cur.fetchone()
                return message.to_json()

        except Exception as e:
            print(e)
            self.con.rollback()
            return e

    def get_message(self, id=None, random=False, type="text"):
        try:
            with self.con:
                cur = self.con.cursor(Model = BotMessage )
                if not random:
                    sql = "SELECT * FROM bot_messages WHERE id=%s"
                    cur.execute(sql, id)
                else:
                    sql = "SELECT * FROM bot_messages WHERE type=%s ORDER BY RAND() LIMIT 1"
                    cur.execute(sql, type)

                message = cur.fetchone()

                if message:
                    return message.to_json()
                return None
        except Exception as e:
            print(e)
            return e.get_error()

    def delete_message(self, id):
        try:
            with self.con:
                cur = self.con.cursor(Model = BotMessage)
                sql = "DELETE FROM bot_messages WHERE id=%s"
                cur.execute(sql, id)
                self.con.commit()

                return self.list_messages()

        except Exception as e:
            print(e)
            self.con.rollback()
            return e

    def list_messages(self, type=None):
        try:
            with self.con:
                cur = self.con.cursor(Model = BotMessage )

                type_lookup = f"WHERE type='{type}'" if type else ""
                sql = f"SELECT * FROM bot_messages {type_lookup}"
                cur.execute(sql)

                messages = cur.fetchall()

                list = {}
                count = 0
                for message in messages:
                    list[count] = message.to_json()
                    count +=1

                return list
        except Exception as e:
            print(e)
            return e.get_error()

    def parse_question(self, message, sender_psid):
        if message is None:
            return False

        if "créer question" in message:
            user = UserView().get_user_from_fb(sender_psid)

            if user is None or not user.to_json()['isAdmin']:
                return True
            array = message.split('\n')
            array.pop(0)
            question = array.pop(0).replace('+ ', '')

            data = {
                'question': question,
                'answers': []
            }

            for response in array:
                response = response.replace('- ','').split('::')
                score = response[1] if len(response)==2 else 0
                response = response[0]
                data['answers'].append({ 'response': response, 'score': score })
            try:
                question = create_question(data)
                response = {
                    "text": "Ta question a bien été enregistrée"
                }
                self.callSendAPI(sender_psid, response)
                return True
            except Exception as e:
                print(e)
                return False

    def send_question(self, sender_psid):
        question = send_question()
        if question is None:
            return

        q = question.get('question')
        q_id = question.get('id')
        answers = question.get('answers', [])

        buttons = []
        for key in answers:
            answer = answers[key]
            buttons.append({
                "title": answer.get('response'),
                "payload": f"@question::{q_id},{answer.get('id')}",
                "type": "postback"
            })

        response = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": q,
                        "buttons": buttons
                    }]
                }
            }
        }
        self.callSendAPI(sender_psid, response)

    def send_stats(self, sender_psid):
        questions = list_question()
        if questions is None:
            print('ah non')
            return

        buttons = []
        for key in questions:
            question = questions[key]
            buttons.append({
                "title": question.get('question'),
                "payload": f"@stats::{question.get('id')}",
                "type": "postback"
            })

        response = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Récupère les statistique pour une question !",
                        "buttons": buttons
                    }]
                }
            }
        }

        self.callSendAPI(sender_psid, response)

    def handle_postback(self, postback, sender_psid):
        if postback is None:
            return
        user = UserView().get_user_from_fb(sender_psid)
        user = user.to_json()

        payload = postback.get('payload')
        payload = payload.split('::')

        payload_type = payload[0]
        value = payload[1]

        if payload_type == "@question":
            value = value.split(',')
            q_id = value[0]
            a_id = value[1]
            data = {
                'q_id': q_id,
                'a_id': a_id,
                'login': user.get('login')
            }
            stats = add_answer(data)

            statssent = ""
            if stats:
                for key in stats:
                    statssent += f"- {stats[key].get('response')}: {stats[key].get('stats', 0)*100}% \n"
            response = {
                    "text": f"Statistiques de la question : \n{statssent}"
            }
            self.callSendAPI(sender_psid, response)

        if payload_type == "@stats":
            stats = answers_stats(value)
            statssent = ""
            if stats:
                for key in stats:
                    statssent += f"- {stats[key].get('response')}: {stats[key].get('stats', 0)*100}% \n"
            response = {
                    "text": f"Statistiques de la question : \n{statssent}"
            }
            self.callSendAPI(sender_psid, response)
