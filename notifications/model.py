class NotificationMessage:
    def __init__(self, data):
        """
        A string title
        """
        self.title = data.get('title')
        """
        string body to display
        """
        self.body = data.get('text')
        """
        A JSON object delivered to your app
        """
        self.data = data.get('data') or None
        """
        when app is in background
        """
        self.display_in_foreground = True

    def to_json(self):
        return {
            'title': self.title,
            'body': self.body,
            'data': self.data,
            'display_in_foreground': self.display_in_foreground
        }
