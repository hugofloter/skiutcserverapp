class Group:
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.owner = data[2]
        self.beer_call = data[3].strftime("%m-%d-%Y %H:%M:%S")

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner': self.owner,
            'beer_call': self.beer_call
        }


class UserGroup:
    def __init__(self, data):
        self.login_user = data[0]
        self.id_group = data[1]
        self.status = data[2]
        self.share_position = data[3],
        self.expiration_date = data[4]

    def to_json(self):
        return {
            'login_user': self.login_user,
            'id_group': self.id_group,
            'status': self.status,
            'share_position': self.share_position,
            'expiration_date': self.expiration_date
        }
