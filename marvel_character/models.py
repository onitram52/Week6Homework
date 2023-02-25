from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

# Adding Flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import secrets to generate user token (how we associate a user with a collection of drones)
import secrets

#flask login to check for authenticated user
from flask_login import UserMixin, LoginManager

#import for flask marshmallow
from flask_marshmallow import Marshmallow

# Create an instance of SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager() #<-- do not forget parenthesis
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref = 'owner', lazy = True)

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

class Character(db.Model):
    id = db.Column(db.String, primary_key = True, default=str(secrets.token_urlsafe))
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String(150))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, comics_appeared_in, super_power, date_created, user_token, id = None):
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.date_created = date_created
        self.user_token = user_token

    def __repr__(self):
        return f"The following character has been added: {self.name}"


class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'comics_appeared_in', 'super_power', 'date_created']

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)
