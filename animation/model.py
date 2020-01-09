class AnimationUser:
    def __init__(self, data):
        self.login_user = data.get('login_user')
        self.level = data.get('level')

    def to_json(self):
        return {
            'login_user': self.login_user,
            'level': self.level
        }


class AnimationKey:
    def __init__(self, data):
        self.key = data.get('key')
        self.level = data.get('level')
        self.next_indice = data.get('next_indice')

    def to_json(self):
        return {
            'key': self.key,
            'level': self.level,
            'next_indice': self.next_indice
        }
