class News():
    def __init__(self, data):
        self.id = data[0]
        self.title = data[1]
        self.text = data[2]
        self.photo = data[3]
        self.date = data[4].strftime("%m-%d-%Y %H:%M:%S")
        self.type = data[5]

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'photo': self.photo,
            'date': self.date,
            'text': self.text,
            'type': self.type,
        }
