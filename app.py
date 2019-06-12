from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os.path
import requests
from datetime import datetime
from forms import RegistrationForm, AddDutyForm
from models import *

DATABASE = "database.db"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_later"

db.app= app

with app.app_context():
    db.init_app(app)


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
    form = AddDutyForm(request.form)
    if request.method == "POST" and form.validate():
        duty_user = form.name.data
        duty_type = form.duty_type.data
        duty_date = form.duty_date.data

        add_new_duty = Duty(duty_user.name, duty_user.lastname, duty_date, duty_type)
        db.session.add(add_new_duty)
        db.session.commit()

    return render_template("addDuty.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        print(form.name.data, form.lastname.data, form.rank.data)
        flash("Ο χρήστης καταχωρήθηκε")

    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
