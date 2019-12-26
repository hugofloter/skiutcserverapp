from bottle import request, response
from bottle import post, put, get
from notifications.view import NotificationsView
from notifications.model import NotificationMessage
from user.view import UserView
from utils.middlewares import authenticate
import json

@post('/notifications')
@authenticate
def send_notifications(user=None):
    """notification center manager"""
    try:
        data = json.loads(request.body.read())
        message_received = data.get('message')
        notification_type = data.get('notification_type')
        if notification_type == "all":
            tokens = UserView().list_tokens()
        else:
            login_list = data.get("login_list")
            tokens = UserView().list_tokens_from_logins(login_list)
        message = NotificationMessage(message_received)
        return NotificationsView(message, tokens).send_push_message()

    except Exception as e:
        return e
