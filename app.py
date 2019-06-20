from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os.path
import requests
from datetime import datetime
from forms import RegistrationForm, AddDutyForm, LoginForm, EditDutyForm, EditUserForm
from models import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from helper_functions import encrypt_password

DATABASE = "database.db"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_later"

db.app = app

with app.app_context():
    db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
# redirect to login page if user is not logged in
login_manager.login_view = "login"
# set a custom message
login_manager.login_message = "Συνδεθείτε στο λογαριασμό σας για να αποκτήσετε πρόσβαση σε αυτή τη σελίδα"

@login_manager.user_loader
def user_loader(user_id):
    return Admin.query.get(int(user_id))

# Create database if it does not exist
if(os.path.exists(DATABASE) == False):
    db.create_all()

    # Add admin with the default login credentails
    admin = Admin()
    admin.add_Admin()

def string_to_datetime(str_input):
    str_input = datetime.strptime(str_input, "%Y-%m-%d")
    return str_input

def user_is_authenticated():
    if current_user.is_authenticated:
        return True
    return False

@app.route("/duties", methods=["GET"])
def duties():
    authorized = user_is_authenticated()
    if request.method == "GET":
        # Get all duties from the database
        duties_list = Duty.query.all()
    return render_template("duties.html", duties_list=duties_list, authorized=authorized)

@app.route("/add_duty", methods=["GET", "POST"])
@login_required
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
@login_required
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
        admin = Admin.query.filter_by(username = form.username.data).first()
        password = form.password.data

        if admin:
            if encrypt_password(password) == admin.password:
                login_user(admin)
                return redirect(url_for("duties"))
            else:
                flash("Το όνομα χρήστη ή ο κωδικός που εισάγατε δεν αντιστοιχεί σε κανέναν λογαριασμό")

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/")
def index():
    return redirect(url_for("duties"))

@app.route("/editDuty/<int:id>", methods=["GET", "POST"])
def editDuty(id):
    form = EditDutyForm(request.form)
    duty = Duty.query.get_or_404(id)

    if request.method == "POST" and form.validate():
        duty.lastname = form.lastname.data.lastname
        duty.duty_type = form.duty_type.data
        duty.duty_date = form.duty_date.data
        duty.name = form.lastname.data.name

        db.session.commit()
        return redirect(url_for("duties"))
    return render_template("edit_duty.html", form=form)

@app.route("/deleteDuty/<int:id>")
def deleteDuty(id):
    duty = Duty.query.get_or_404(id)

    if duty:
        db.session.delete(duty)
        db.session.commit()
    return redirect(url_for("duties"))

@app.route("/users", methods=["GET", "POST"])
@login_required
def users():
    if request.method == "GET":
        users_list = User.query.all()
    return render_template("users.html", users_list=users_list)

@app.route("/editUser/<int:id>", methods=["GET", "POST"])
@login_required
def editUser(id):
    form = EditUserForm(request.form)
    user = User.query.get_or_404(id)

    if request.method == "POST" and form.validate():
        user.name = form.name.data
        user.lastname = form.lastname.data
        user.rank = form.rank.data

        db.session.commit()
        return redirect(url_for("users"))
    return render_template("edit_user.html", form=form)

@app.route("/deleteUser/<int:id>")
@login_required
def deleteUser(id):
    user = User.query.get_or_404(id)

    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("users"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
