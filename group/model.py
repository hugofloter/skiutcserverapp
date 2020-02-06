class Group:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.owner = data.get('owner')
        if data.get('beer_call'):
            self.beer_call = data.get('beer_call').strftime("%m-%d-%Y %H:%M:%S")
        else:
            self.beer_call = None

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner': self.owner,
            'beer_call': self.beer_call
        }


class UserGroup:
    def __init__(self, data):
        self.login_user = data.get('login_user')
        self.id_group = data.get('id_group')
        self.status = data.get('status')
        self.share_position = data.get('share_position')
        if data.get('expiration_date'):
            self.expiration_date = data.get('expiration_date').strftime("%m-%d-%Y %H:%M:%S")
        else:
            self.expiration_date = None

    def to_json(self):
        return {
            'login_user': self.login_user,
            'id_group': self.id_group,
            'status': self.status,
            'share_position': self.share_position,
            'expiration_date': self.expiration_date
        }
