class User():
    def __init__(self, data):
        self.login = data[0]
        self.lastname = data[1]
        self.firstname = data[2]
        self.email = data[3]
        self.password = data[4]
        self.is_admin = data[5]
        self.last_position = data[6]
        self.push_token = data[7]

    def to_json(self):
        return {
            'login': self.login,
            'lastname': self.lastname,
            'firstname': self.firstname,
            'email': self.email,
            'isAdmin': self.is_admin,
            'lastPosition': self.last_position,
            'push_token': self.push_token
        }
