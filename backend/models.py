from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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

# https://stackabuse.com/single-page-apps-with-vue-js-and-flask-jwt-authentication/

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def serialize(self):
        return dict(id=self.id, email=self.email)