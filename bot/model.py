class BotUser():
    def __init__(self, data):
        self.fb_id = data.get('fb_id')
        self.login = data.get('login')
        self.token = data.get('token')
        self.last_action = data.get('last_action')

    def to_json(self):
        return {
            "fb_id": self.fb_id,
            "login": self.login,
            "token": self.token,
            "last_action": self.last_action
        }
