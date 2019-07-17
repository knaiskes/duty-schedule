from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os.path
import requests
from datetime import datetime, timedelta
from datetime import date
from forms import RegistrationForm, AddDutyForm, LoginForm, EditDutyForm, EditUserForm, SearchDuty, DateOptions, GenerateDutieForm, AddNewDutyType, EditDutyType, AddAbsentTypeForm, AddAbsentForm, EditAbsentForm, EditAbsentTypeForm
from models import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from helper_functions import encrypt_password, generateDuties

DATABASE = "database.db"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_later"

db.app = app

with app.app_context():
    db.init_app(app)

def string_to_datetime(str_input):
    str_input = datetime.strptime(str_input, "%Y-%m-%d")
    return str_input

login_manager = LoginManager()
login_manager.init_app(app)
# redirect to login page if user is not logged in
login_manager.login_view = "login"
# set a custom message
login_manager.login_message = "Συνδεθείτε στο λογαριασμό σας για να αποκτήσετε πρόσβαση σε αυτή τη σελίδα"

#list for generate_duties route
users_list_gen = []

@login_manager.user_loader
def user_loader(user_id):
    return Admin.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)

# Create database if it does not exist
if(os.path.exists(DATABASE) == False):
    db.create_all()

    # Add admin with the default login credentails
    admin = Admin()
    admin.add_Admin()

def user_is_authenticated():
    if current_user.is_authenticated:
        return True
    return False

@app.route("/duties", methods=["GET", "POST"])
def duties():
    #cheap solution to clean the user_list_gen list
    #by sending the user back to duties route after submitting
    users_list_gen.clear()
    form = SearchDuty(request.form)
    form_options = DateOptions(request.form)
    authorized = user_is_authenticated()
    query_date = date.today()
    base_msg_form = "Οι υπηρεσίες για "
    msg_form = base_msg_form + "σήμερα " + "(" + query_date.strftime("%d-%m-%Y") + ")"

    if request.method == "POST" and form.validate():
        query_date = form.search_date.data
        duties_list = Duty.query.filter(Duty.duty_date == query_date).all()
        msg_form = base_msg_form + "τις " + query_date.strftime("%d-%m-%Y")

    if request.method == "POST" and form_options.validate() and form_options.submit.data:
        #TODO: a better solution must be implied
        #The current solution is temporary
        if form_options.date_options.data == "all":
            duties_list = Duty.query.order_by(desc(Duty.duty_date)).all()
            msg_form = "Όλες οι υπηρεσίες"
        elif form_options.date_options.data == "week":
            today = datetime.now().date()
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            duties_list = Duty.query.order_by(desc(Duty.duty_date)).filter(Duty.duty_date.between(start,end)).all()
            msg_form = base_msg_form + "την εβδομάδα " + "(" + start.strftime("%d-%m-%Y") + " - " + end.strftime("%d-%m-%Y") + ")"
        elif form_options.date_options.data == "tomorrow":
            from helper_functions import calculateDateQuery
            query_date  = calculateDateQuery(form_options.date_options.data)
            duties_list = Duty.query.filter(Duty.duty_date == query_date).all()
            msg_form = base_msg_form + "αύριο " + "(" + query_date.strftime("%d-%m-%Y") + ")"
        elif form_options.date_options.data == "month":
            import calendar
            today = date.today()
            current_month =  today.month
            current_year = today.year
            month_days = calendar.monthrange(current_year, current_month)[1]
            start = date(current_year, current_month, 1)
            end = date(current_year, current_month, month_days)
            duties_list = Duty.query.order_by(desc(Duty.duty_date)).filter(Duty.duty_date.between(start, end)).all()
            msg_form = base_msg_form + "τον μήνα " + "(" + start.strftime("%d-%m-%Y") + " - " + end.strftime("%d-%m-%Y") + ")"
        else:
            from helper_functions import calculateDateQuery
            query_date  = calculateDateQuery(form_options.date_options.data)
            duties_list = Duty.query.filter(Duty.duty_date == query_date).all()

    if request.method == "GET":
        duties_list = Duty.query.filter(Duty.duty_date == query_date).all()
        msg_form = base_msg_form + "σήμερα " + "(" + query_date.strftime("%d-%m-%Y") + ")"

    return render_template("duties.html", duties_list=duties_list,
            authorized=authorized, msg_form=msg_form,
            form=form, form_options=form_options)

@app.route("/add_duty", methods=["GET", "POST"])
@login_required
def add_duty_form():
    form = AddDutyForm(request.form)
    if request.method == "POST" and form.validate():
        duty_user = form.lastname.data
        duty_type = form.duty_type.data
        duty_date = form.duty_date.data

        add_new_duty = Duty(duty_user.name, duty_user.lastname, duty_date, duty_type.name, duty_user.rank)
        db.session.add(add_new_duty)
        db.session.commit()

        flash("Η υπηρεσία προστέθηκε")

    return render_template("addDuty.html", form=form)

@app.route("/add_duty_type", methods=["GET", "POST"])
@login_required
def add_duty_type():
    form = AddNewDutyType(request.form)
    if request.method == "POST" and form.validate():
        add_new_duty_type = Duty_types(form.name.data)
        db.session.add(add_new_duty_type)
        db.session.commit()
        flash("Ο νέος τύπος υπηρεσίας καταχωρήθηκε")

    return render_template("addDutyType.html", form=form)

@app.route("/generate_duties", methods=["GET","POST"])
@login_required
def generate_duties():
    form = GenerateDutieForm(request.form)
    if request.method == "POST" and form.add.data:
        users_list_gen.append(form.lastname.data)
    if request.method == "POST" and form.clear.data:
        users_list_gen.clear()
    if request.method == "POST" and form.submit.data and form.validate():
        date_options = form.date_options.data
        duty_type = form.duty_type.data
        users_generate = generateDuties(users_list_gen, date_options)
        for i in users_generate:
            rank = i[0].rank
            name = i[0].name
            lastname = i[0].lastname
            date_options = i[1]
            print(rank, name, lastname, date_options, duty_type)
            add_new_duty = Duty(name, lastname, date_options, duty_type.name, rank)
            db.session.add(add_new_duty)
            db.session.commit()
        return redirect(url_for("duties"))
    return render_template("generateDuties.html", form=form, users=users_list_gen)

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

    if request.method == "GET":
        form.duty_date.data = string_to_datetime(duty.duty_date.strftime("%Y-%m-%d"))
        form.duty_type.data = duty.duty_type

    if request.method == "POST" and form.validate():
        duty.lastname = form.lastname.data.lastname
        duty.duty_type = form.duty_type.data.name
        duty.duty_date = form.duty_date.data
        duty.name = form.lastname.data.name
        duty.rank = form.lastname.data.rank

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

    if request.method == "GET":
        form.name.data = user.name
        form.lastname.data = user.lastname
        form.rank.data = user.rank

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

@app.route("/duties_type_list", methods=["GET", "POST"])
@login_required
def duties_type_list():
    if request.method == "GET":
        duties_type_list = Duty_types.query.all()
    return render_template("duties_type_list.html", duties_type_list=duties_type_list)

@app.route("/delete_duty_type/<int:id>")
@login_required
def delete_duty_type(id):
    duty_type = Duty_types.query.get_or_404(id)

    if duty_type:
        db.session.delete(duty_type)
        db.session.commit()
    return redirect(url_for("duties_type_list"))

@app.route("/edit_duty_type/<int:id>", methods=["GET", "POST"])
@login_required
def edit_duty_type(id):
    form = EditDutyType(request.form)
    duty_type = Duty_types.query.get_or_404(id)

    if request.method == "GET":
        form.name.data = duty_type.name

    if request.method == "POST" and form.validate():
        duty_type.name = form.name.data
        db.session.commit()
        return redirect(url_for("duties_type_list"))
    return render_template("edit_duty_type.html", form=form)

@app.route("/absent_list", methods=["GET", "POST"])
@login_required
def absent_list():
    if request.method == "GET":
        absent_list = Absent.query.all()
    return render_template("absent_list.html", absent_list=absent_list)

@app.route("/add_absent", methods=["GET", "POST"])
@login_required
def add_absent():
    form = AddAbsentForm(request.form)
    if request.method == "POST" and form.validate():
        absent_user_name = form.lastname.data
        absent_type = form.absent_type.data
        absent_days = form.days.data
        absent_start = form.start.data
        absent_end = form.end.data

        add_new_absent = Absent(absent_type.name, absent_days,
                absent_user_name.name, absent_user_name.lastname,
                absent_user_name.rank, absent_start, absent_end)
        db.session.add(add_new_absent)
        db.session.commit()
        flash("Η άδεια καταχωρήθηκε")
    return render_template("add_absent.html", form=form)

@app.route("/editAbsent/<int:id>", methods=["GET", "POST"])
@login_required
def editAbsent(id):
    form = EditAbsentForm(request.form)
    absent = Absent.query.get_or_404(id)

    if request.method == "GET":
        form.start.data = string_to_datetime(absent.start.strftime("%Y-%m-%d"))
        form.end.data = string_to_datetime(absent.end.strftime("%Y-%m-%d"))
        form.days.data = absent.days

    if request.method == "POST" and form.validate():
        absent.lastname = form.lastname.data.lastname
        absent.name = form.lastname.data.name
        absent.absent_type = form.absent_type.data.name
        absent.rank = form.lastname.data.rank
        absent.days = form.days.data
        absent.start = form.start.data
        absent.end = form.end.data

        db.session.commit()
        return redirect(url_for("absent_list"))

    return render_template("editAbsent.html", form=form)

@app.route("/deleteAbsent/<int:id>", methods=["GET", "POST"])
@login_required
def deleteAbsent(id):
    absent = Absent.query.get_or_404(id)
    if absent:
        db.session.delete(absent)
        db.session.commit()
    return redirect(url_for("absent_list"))

@app.route("/add_absent_type", methods=["GET", "POST"])
@login_required
def add_absent_type():
    form = AddAbsentTypeForm(request.form)
    if request.method == "POST" and form.validate():
        add_new_absent_type = Absent_types(form.name.data)
        db.session.add(add_new_absent_type)
        db.session.commit()
        flash("Ο νέος τύπος άδειας καταχωρήθηκε")

    return render_template("add_absent_type.html", form=form)

@app.route("/absent_types_list", methods=["GET", "POST"])
@login_required
def absent_types_list():
    if request.method == "GET":
        absent_types_list = Absent_types.query.all()
    return render_template("absent_types_list.html", absent_types_list=absent_types_list)

@app.route("/editAbsentType/<int:id>", methods=["GET", "POST"])
@login_required
def editAbsentType(id):
    form = EditAbsentTypeForm(request.form)
    absent = Absent_types.query.get_or_404(id)

    if request.method == "GET":
        form.name.data = absent.name

    if request.method == "POST" and form.validate():
        absent.name = form.name.data

        db.session.commit()
        return redirect(url_for("absent_types_list"))

    return render_template("editAbsentType.html", form=form)

@app.route("/deleteAbsentType/<int:id>", methods=["GET", "POST"])
@login_required
def deleteAbsentType(id):
    absent = Absent_types.query.get_or_404(id)
    if absent:
        db.session.delete(absent)
        db.session.commit()
    return redirect(url_for("absent_types_list"))

@app.route("/month_table", methods=["GET", "POST"])
@login_required
def month_table():
    #result = db.session.query(Duty.name).join(User, User.name == Duty.name)
    #result = db.session.query(Duty).join(Absent)
    import calendar
    today = date.today()
    current_month =  today.month
    current_year = today.year
    month_days = calendar.monthrange(current_year, current_month)[1]
    start = date(current_year, current_month, 1)
    end = date(current_year, current_month, month_days)

    duties_list = Duty.query.order_by(desc(Duty.duty_date)).filter(Duty.duty_date.between(start, end)).all()
    absent_list = Absent.query.order_by(desc(Absent.start)).filter(Absent.start.between(start, end)).all()

    return render_template("month_table.html", duties_list=duties_list, absent_list=absent_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
