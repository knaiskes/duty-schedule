from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(10))

    def __init__(self):
        # Default login credentials
        # TODO in the first run of the app make user change the default password
        self.username = "admin"
        self.password = "admin"

    def add_Admin(self):
        db.session.add(Admin())
        db.session.commit()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    rank = db.Column(db.String(15))

    def __init__(self, name, lastname, rank):
        self.name = name
        self.lastname = lastname
        self.rank = rank

class Duty(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    duty_date = db.Column(db.Date)
    duty_type = db.Column(db.String(30))

    def __init__(self, name, lastname, duty_date, duty_type):
        self.name = name
        self.lastname = lastname
        self.duty_date = duty_date
        self.duty_type = duty_type
