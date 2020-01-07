class News():
    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.text = data.get('text')
        self.img_url = data.get('img_url')
        self.img_width = data.get('img_width')
        self.img_height = data.get('img_height')
        self.date = data.get('date').strftime("%m-%d-%Y %H:%M:%S")
        self.type = data.get('type')

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
