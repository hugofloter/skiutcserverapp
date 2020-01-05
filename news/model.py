class News():
    def __init__(self, data):
        self.id = data[0]
        self.title = data[1]
        self.text = data[2]
        self.img_url = data[3]
        self.img_width = data[4]
        self.img_height = data[5]
        self.date = data[6].strftime("%m-%d-%Y %H:%M:%S")
        self.type = data[7]

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'img_url': self.img_url,
            'img_width': self.img_width,
            'img_height': self.img_height,
            'date': self.date,
            'text': self.text,
            'type': self.type,
        }
