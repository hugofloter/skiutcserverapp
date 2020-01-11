class BotTokenChallenge:
    def __init__(self, data):
        self.token = data.get('token')
        self.challenge = data.get('challenge')

    def to_json(self):
        return {
            'token': self.token,
            'challenge': self.challenge
        }
