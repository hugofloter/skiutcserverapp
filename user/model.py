class User():
    def __init__(self, data):
        self.login = data.get('login')
        self.lastname = data.get('lastname')
        self.firstname = data.get('firstname')
        self.email = data.get('email')
        self.password = data.get('password')
        self.is_admin = data.get('isAdmin')
        self.last_position = {
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude')
        }
        self.push_token = data.get('push_token');
        self.avatar = {
            'img_url': data.get('img_url'),
            'img_width': data.get('img_width'),
            'img_height': data.get('img_height'),
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
