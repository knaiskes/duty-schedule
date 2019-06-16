from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os.path
import requests
from datetime import datetime
from forms import RegistrationForm, AddDutyForm, LoginForm
from models import *
from flask_login import LoginManager, login_user, login_required, logout_user

DATABASE = "database.db"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_later"

db.app= app

with app.app_context():
    db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

# Create database if it does not exist
if(os.path.exists(DATABASE) == False):
    db.create_all()

def string_to_datetime(str_input):
    str_input = datetime.strptime(str_input, "%Y-%m-%d")
    return str_input

@app.route("/duties", methods=["GET"])
@login_required
def duties():
    if request.method == "GET":
        # Get all duties from the database
        duties_list = Duty.query.all()
    return render_template("duties.html", duties_list=duties_list)

@app.route("/add_duty", methods=["GET", "POST"])
def add_duty_form():
    form = AddDutyForm(request.form)
    if request.method == "POST" and form.validate():
        duty_user = form.lastname.data
        duty_type = form.duty_type.data
        duty_date = form.duty_date.data

        add_new_duty = Duty(duty_user.name, duty_user.lastname, duty_date, duty_type)
        db.session.add(add_new_duty)
        db.session.commit()

        flash("Η υπηρεσία προστέθηκε")

    return render_template("addDuty.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        new_user = User(form.name.data, form.lastname.data, form.rank.data)
        db.session.add(new_user)
        db.session.commit()

        flash("Ο χρήστης καταχωρήθηκε")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(name = form.name.data).first()
        if user:
            login_user(user)
            return redirect(url_for("duties"))

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
