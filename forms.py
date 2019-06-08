from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField("Όνομα χρήστη",
            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Διεύθυνση email",
            validators=[DataRequired(), Email()])
    password = PasswordField("Κωδικός", validators=[DataRequired()])
    confirm = PasswordField("Επαλήθευση κωδικού",
            validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("submit")
