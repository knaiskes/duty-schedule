from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
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
    return User.query.distinct(User.name).group_by(User.name).all()

class AddDutyForm(FlaskForm):
    name = QuerySelectField(query_factory = user_query, get_label="name")
    submit = SubmitField("submit")
