from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os.path
import requests
import json
from datetime import datetime
from forms import RegistrationForm

DATABASE = "database.db"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_later"

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)

headers = {"Content-type": "application/json", "Accept": "text/plain"}
api_url = "http://localhost:5000/api.duties"

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

class DutySchema(marshmallow.Schema):
    class Meta:
        fields = ("id", "name", "lastname", "duty_date", "duty_type")

duty_schema = DutySchema(strict = True)
duties_schema = DutySchema(many = True, strict = True)

def string_to_datetime(str_input):
    str_input = datetime.strptime(str_input, "%Y-%m-%d")
    return str_input

# API

@app.route("/api.duties", methods=["GET"])
def get_all_duties():
    all_duties = Duty.query.all()
    all_duties = duties_schema.dump(all_duties)
    return jsonify(all_duties.data)

@app.route("/api.duties", methods=["POST"])
def add_duty():
    name = request.json["name"]
    lastname = request.json["lastname"]
    duty_date = request.json["duty_date"]
    duty_date = string_to_datetime(duty_date)
    duty_type = request.json["duty_type"]

    add_new_duty = Duty(name, lastname, duty_date, duty_type)
    db.session.add(add_new_duty)
    db.session.commit()

    return duty_schema.jsonify(add_new_duty)

@app.route("/api.duties/<id>", methods=["PUT"])
def update_duty(id):
    update_a_duty = Duty.query.get(id)

    name = request.json["name"]
    lastname = request.json["lastname"]
    duty_date = request.json["duty_date"]
    duty_date = string_to_datetime(duty_date)
    duty_type = request.json["duty_type"]

    update_a_duty.name = name
    update_a_duty.lastname = lastname
    update_a_duty.duty_date = duty_date
    update_a_duty.duty_type = duty_type

    db.session.commit()

    return duty_schema.jsonify(update_a_duty)

@app.route("/api.duties/<id>", methods=["DELETE"])
def delete_duty(id):
    delete_a_duty = Duty.query.get(id)
    db.session.delete(delete_a_duty)
    db.session.commit()

    return duty_schema.jsonify(delete_a_duty)

@app.route("/duties", methods=["GET"])
def duties():
    if request.method == "GET":
        duties_list = requests.get(api_url)
        duties_list = duties_list.json()
    return render_template("duties.html", duties_list=duties_list)

@app.route("/add_duty", methods=["GET", "POST"])
def add_duty_form():
    if request.method == "POST":
        name = request.form["name"]
        lastname = request.form["lastname"]
        duty_date = request.form["duty_date"]
        duty_type= request.form["duty_type"]

        #duty_date = string_to_datetime(duty_date)

        data = {"name": name, "lastname": lastname, "duty_date": duty_date,
                "duty_type": duty_type}
        add_duty = requests.post(api_url, data = json.dumps(data), headers = headers)
    return render_template("addDuty.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        print(form.username.data, form.email.data, form.password.data)
        flash("Ο χρήστης καταχωρήθηκε")

    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
