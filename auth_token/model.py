class AuthToken ():
    def __init__(self, data):
        self.login = data[0]
        self.token = data[1]

    def to_json(self):
        return {
            'login': self.login,
            'token': self.token
        }
