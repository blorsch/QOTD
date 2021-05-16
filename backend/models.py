from app import db

# https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/

class Quote(db.Model):
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String())
    author = db.Column(db.String())

    def __init__(self, text, author):
        self.text = text
        self.author = author

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'text': self.text,
            'author':self.author
        }