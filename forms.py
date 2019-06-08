from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField("Όνομα",
            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField("Επώνυμο", validators=[DataRequired(),
        Length(min=2, max=20)])
    password = PasswordField("Κωδικός", validators=[DataRequired()])
    confirm = PasswordField("Επαλήθευση κωδικού",
            validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("submit")
