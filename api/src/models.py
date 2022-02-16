from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    surname = db.Column(db.String(90), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    def __init__(self, name, surname, email, password, role="client"):
        self.name = name
        self.surname = surname
        self.email = email
        self.hash_password(password)
        self.role = role

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "role": self.role,
        }

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        try:
            if check_password_hash(self.password, password):
                return True
        except:
            return False


class Products(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String)
    price = db.Column(db.Float)

    def __init__(self, name, description=None, price=None):
        self.name = name
        self.description = description
        self.price = price
