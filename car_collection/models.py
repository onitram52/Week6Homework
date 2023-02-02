from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import UserMixin, LoginManager

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = 'owner', lazy = True)

    def __init__(self, email, password, first_name = '', last_name = '', id = '', token = ''):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.token = self.set_token(24)


    def set_id(self):
        return str(uuid.uuid4())

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added to the database!"

class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    nickname = db.Column(db.String(150))
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(precision=8, scale=2))
    color = db.Column(db.String(150))
    horsepower = db.Column(db.String(150))
    max_speed = db.Column(db.String(150))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    cost_of_production = db.Column(db.Numeric(precision=12, scale=2))
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, nickname, description, price, color, horsepower, max_speed, dimensions, weight, cost_of_production, make, model, user_token, id = ''):
        self.id = self.set_id()
        self.nickname = nickname
        self.description = description
        self.price = price
        self.color = color
        self.horsepower = horsepower
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_production = cost_of_production
        self.make = make
        self.model = model
        self.user_token = user_token

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"The following car has been added: {self.name}"


class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'nickname', 'description', 'price', 'color', 'horsepower', 'max_speed', 'dimensions', 'weight', 'cost_of_production', 'make', 'model',]

car_schema = CarSchema()
cars_schema = CarSchema(many=True)
