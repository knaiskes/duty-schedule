from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    lastname = db.Column(db.String(30))

    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname

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
