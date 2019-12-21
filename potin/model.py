
#Potin( id int, title string, text string, approve boolean, user fk(user), anonymous boolean)

class Potin():
    def __init__(self, id, title, text, approved, user, anonymous):
        self.id = id

