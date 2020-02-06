class Potin():
    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.text = data.get('text')
        self.approved = data.get('approved')
        self.sender = data.get('sender')
        self.isAnonymous = data.get('isAnonymous')

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'approved': self.approved,
            'sender': self.sender,
            'isAnonymous': self.isAnonymous
        }
