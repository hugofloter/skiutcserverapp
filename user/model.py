class User():
    def __init__(self, data):
        self.login = data[0]
        self.lastname = data[1]
        self.firstname = data[2]
        self.email = data[3]
        self.password = data[4]
        self.is_admin = data[5]
        self.last_position = {
            'latitude': data[6],
            'longitude': data[7]
        }
        self.push_token = data[8],
        self.avatar = {
            'img_url': data[9],
            'img_width': data[10],
            'img_weight': data[11],
        }

    def to_json(self):
        return {
            'login': self.login,
            'lastname': self.lastname,
            'firstname': self.firstname,
            'email': self.email,
            'isAdmin': self.is_admin,
            'avatar': self.avatar
        }

    def get_push_token(self):
        return self.push_token


class Location:
    def __init__(self, data):
        self.latitude = data.get('latitude')
        self.longitude = data.get('longitude')

    def to_json(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude
        }
