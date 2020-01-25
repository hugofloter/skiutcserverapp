class BotUser():
    def __init__(self, data):
        self.fb_id = data.get('fb_id')
        self.login = data.get('login')
        self.token = data.get('token')
        self.last_action = data.get('last_action')

    def to_json(self):
        return {
            "fb_id": self.fb_id,
            "login": self.login,
            "token": self.token,
            "last_action": self.last_action
        }


class BotMessage():
    def __init__(self, data):
        self.id = data.get('id')
        self.text = data.get('text')
        self.type = data.get('type')

    def to_json(self):
        return {
            "id": self.id,
            "text": self.text,
            "type": self.type
        }


class BotQuestion():
    def __init__(self, data):
        self.id = data.get('id')
        self.question = data.get('question')
        self.sent = data.get('sent')

    def to_json(self):
        return {
            "id": self.id,
            "question": self.question,
            "sent": self.sent
        }


class BotAnswer():
    def __init__(self, data):
        self.id = data.get('id')
        self.question_id = data.get('question_id')
        self.answer = data.get('answer')
        self.score = data.get('score')

    def to_json(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "answer": self.answer,
            "score": self.score
        }


class UserAnswer():
    def __init__(self, data):
        self.login = data.get('login')
        self.question_id = data.get('question_id')
        self.answer_id = data.get('answer_id')

    def to_json(self):
        return {
            "login": self.login,
            "question_id": self.question_id,
            "answer_id": self.answer_id
        }
