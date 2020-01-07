class AuthToken ():
    def __init__(self, data):
        self.login = data.get('login')
        self.token = data.get('token')

    def to_json(self):
        return {
            'login': self.login,
            'token': self.token
        }
