class Potin():
    def __init__(self, data):
        self.id = data[0]
        self.title = data[1]
        self.text = data[2]
        self.approved = data[3]
        self.sender = data[4]
        self.isAnonymous = data[5]

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'approved': self.approved,
            'sender': self.sender,
            'isAnonymous': self.isAnonymous
        }
