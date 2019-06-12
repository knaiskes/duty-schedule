from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from models import User

class RegistrationForm(FlaskForm):
    name = StringField("Όνομα",
            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField("Επώνυμο", validators=[DataRequired(),
        Length(min=2, max=20)])
    password = PasswordField("Κωδικός", validators=[DataRequired()])
    confirm = PasswordField("Επαλήθευση κωδικού",
            validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("submit")

def user_query():
    return User.query.distinct(User.lastname).group_by(User.lastname).all()

class AddDutyForm(FlaskForm):
    lastname = QuerySelectField(query_factory = user_query, get_label="lastname")
    duty_type = SelectField("Τύπος υπηρεσίας",
            choices = [("ΚΕΗΠ","ΚΕΗΠ"), ("ΦΥΛΑΚΙΟ", "ΦΥΛΑΚΙΟ")])
    duty_date = DateField("Ημερομηνία", format="%Y-%m-%d")
    submit = SubmitField("submit")
