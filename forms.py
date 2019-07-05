from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField,IntegerField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from models import User

class RegistrationForm(FlaskForm):
    name = StringField("Όνομα",
            validators=[DataRequired(), Length(min=2, max=20)],
            render_kw={"placeholder": "Όνομα"})
    lastname = StringField("Επώνυμο", validators=[DataRequired(),
        Length(min=2, max=20)], render_kw={"placeholder": "Επώνυμο"})
    rank = SelectField("Βαθμός", choices = [("Στρατιώτης","Στρατιώτης"),
        ("Υποδεκανέας","Υποδεκανέας"), ("Δεκανέας", "Δεκανέας"),
        ("Λοχίας", "Λοχίας"), ("Επιλοχίας", "Επιλοχίας"),
        ("Αρχιλοχίας", "Αρχιλοχίας"), ("Ανθυπασπιστής", "Ανθυπασπιστής"),
        ("Δόκιμος Έφεδρος Αξιωματικός", "Δόκιμος Έφεδρος Αξιωματικός")])
    submit = SubmitField("Προσθήκη")

class EditUserForm(FlaskForm):
    name = StringField("Όνομα",
            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField("Επώνυμο", validators=[DataRequired(),
        Length(min=2, max=20)])
    rank = SelectField("Βαθμός", choices = [("Στρατιώτης","Στρατιώτης"),
        ("Υποδεκανέας","Υποδεκανέας"), ("Δεκανέας", "Δεκανέας"),
        ("Λοχίας", "Λοχίας"), ("Επιλοχίας", "Επιλοχίας"),
        ("Αρχιλοχίας", "Αρχιλοχίας"), ("Ανθυπασπιστής", "Ανθυπασπιστής"),
        ("Δόκιμος Έφεδρος Αξιωματικός", "Δόκιμος Έφεδρος Αξιωματικός")])
    submit = SubmitField("Αποθήκευση αλλαγών")

class LoginForm(FlaskForm):
    username = StringField("Όνομα χρήστη", validators=[DataRequired()],
            render_kw={"placeholder": "Όνομα χρήστη"})
    password = PasswordField("Κωδικός", validators=[DataRequired()],
            render_kw={"placeholder": "Κωδικός"})
    submit = SubmitField("Είσοδος")

def user_query():
    #return User.query.distinct(User.lastname).group_by(User.lastname).all()
    return User.query.all()

class AddDutyForm(FlaskForm):
    lastname = QuerySelectField("Ονοματεπώνυμο",
            query_factory = user_query, get_label=lambda user:
            user.lastname + " " + user.name)
    duty_type = SelectField("Τύπος υπηρεσίας",
            choices = [("ΚΕΕΗΠ","ΚEΕΗΠ"), ("ΦΥΛΑΚΙΟ", "ΦΥΛΑΚΙΟ")])
    duty_date = DateField("Ημερομηνία", format="%Y-%m-%d")
    submit = SubmitField("Προσθήκη")

class EditDutyForm(FlaskForm):
    lastname = QuerySelectField("Ονοματεπώνυμο", query_factory = user_query,
            get_label=lambda user: user.lastname + " " + user.name)
    duty_type = SelectField("Τύπος υπηρεσίας",
            choices = [("ΚΕΕΗΠ","ΚEΕΗΠ"), ("ΦΥΛΑΚΙΟ", "ΦΥΛΑΚΙΟ")])
    duty_date = DateField("Ημερομηνία", format="%Y-%m-%d")
    submit = SubmitField("Αποθήκευση αλλαγών")

class SearchDuty(FlaskForm):
    search_date = DateField("Ημερομηνία", format="%Y-%m-%d",
            validators=[DataRequired()])
    submit = SubmitField("Αναζήτηση")

class DateOptions(FlaskForm):
    date_options = SelectField("Επιλογές",
            choices=[("today", "Σήμερα"),
                ("tomorrow", "Αύριο"),("week", "Εβδομάδα"), ("month", "Μήνας"), ("all", "Όλες")])
    submit = SubmitField("Αναζήτηση")

class GenerateDutieForm(FlaskForm):
    lastname = QuerySelectField(query_factory = user_query, get_label=lambda user:
            user.lastname + " " + user.name)
    add = SubmitField("Προσθήκη")
    clear = SubmitField("clear")
    duty_type = SelectField("Τύπος υπηρεσίας",
            choices = [("ΚΕΕΗΠ","ΚEΕΗΠ"), ("ΦΥΛΑΚΙΟ", "ΦΥΛΑΚΙΟ")])
    days = IntegerField("Ημέρες")
    submit = SubmitField("submit")
