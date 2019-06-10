from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os.path
import requests
from datetime import datetime
from forms import RegistrationForm

DATABASE = "database.db"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_later"

db = SQLAlchemy(app)

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

def string_to_datetime(str_input):
    str_input = datetime.strptime(str_input, "%Y-%m-%d")
    return str_input

@app.route("/duties", methods=["GET"])
def duties():
    if request.method == "GET":
        # Get all duties from the database
        duties_list = Duty.query.all()
    return render_template("duties.html", duties_list=duties_list)

@app.route("/add_duty", methods=["GET", "POST"])
def add_duty_form():
    if request.method == "POST":
        name = request.form["name"]
        lastname = request.form["lastname"]
        duty_date = request.form["duty_date"]
        duty_type= request.form["duty_type"]

        duty_date = string_to_datetime(duty_date)

        add_new_duty = Duty(name, lastname, duty_date, duty_type)
        db.session.add(add_new_duty)
        db.session.commit()

    return render_template("addDuty.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        print(form.name.data, form.lastname.data, form.password.data)
        flash("Ο χρήστης καταχωρήθηκε")

    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
