from app import db

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cookie = db.Column(db.String(128), index=True, unique=True)
    first_visit = db.Column(db.Integer, index=True)
    counter = db.Column(db.Integer)

    def __repr__(self):
        return '<Visitor: {} visited {} times.>'.format(self.cookie, self.counter)



class Message(db.Model):
    """
    Store a simple message.
    """

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, index=True)
    message = db.Column(db.String)

    def __init__(self, author, message):
        """
        Create a message.

        Args:
            author: The authors email
            message: The message text
        """
        self.author = author
        self.message = message

    def ___repr__(self):
        """
        Representation of the message.
        """
        return "<author: {} message: {}".format(self.author, self.message)

