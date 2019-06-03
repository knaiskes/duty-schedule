from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os.path
import requests
import json
from datetime import datetime

DATABASE = "database.db"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)

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
    # Convert str date to Python date object
    duty_date = datetime.strptime(duty_date, "%Y-%m-%d")
    duty_type = request.json["duty_type"]

    add_new_duty = Duty(name, lastname, duty_date, duty_type)
    db.session.add(add_new_duty)
    db.session.commit()

    return duty_schema.jsonify(add_new_duty)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
