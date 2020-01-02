from db import dbskiutc_con as db
from exponent_server_sdk import DeviceNotRegisteredError, PushClient,PushMessage, PushResponseError, PushServerError
from requests.exceptions import ConnectionError, HTTPError


#@TODO return error to d=response.code and so on...
class NotificationsView():
    def __init__(self, message, tokens):
        self.con = db()
        self.message = message.to_json()
        self.tokens = tokens
        self.publishmessagelist = []
        self.build_publish_messages()

    def build_publish_messages(self):
        for token in self.tokens:
            new_publish = PushMessage(to=token, body=self.message.get('body'),
                                      title=self.message.get('title'),
                                      display_in_foreground=self.message.get('display_in_foreground'))
            self.publishmessagelist.append(new_publish)

    def send_push_message(self):
        try:
            responses = PushClient().publish_multiple(self.publishmessagelist)

        except PushServerError as exc:
            print("pushservererror", exc)
            raise

        except (ConnectionError, HTTPError) as exc:
            print("connection error ", exc)
            raise

        try:
            # We got a response back, but we don't know whether it's an error yet.
            # This call raises errors so we can handle them with normal exception
            # flows.
            for response in responses:
                response.validate_response()
            return responses

        except PushResponseError as exc:
            # Encountered some other per-notification error.
            print("pushresponse failed > ", exc)
            raise
