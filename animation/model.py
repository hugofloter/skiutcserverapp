class AnimationUser:
    def __init__(self, data):
        self.login_user = data.get('login_user')
        self.level = data.get('level')

    def to_json(self):
        return {
            'login_user': self.login,
            'level': self.level
        }
