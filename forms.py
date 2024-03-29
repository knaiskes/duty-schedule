from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField,IntegerField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from models import User
from models import Duty_types, Absent_types

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
        ("Δόκιμος Έφεδρος Αξιωματικός", "Δόκιμος Έφεδρος Αξιωματικός"),
        ("Ανθυπολοχαγός", "Ανθυπολοχαγός"), ("Υπολοχαγός", "Υπολοχαγός"),
        ("Λοχαγός", "Λοχαγός")])
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
        ("Δόκιμος Έφεδρος Αξιωματικός", "Δόκιμος Έφεδρος Αξιωματικός"),
        ("Ανθυπολοχαγός", "Ανθυπολοχαγός"), ("Υπολοχαγός", "Υπολοχαγός"),
        ("Λοχαγός", "Λοχαγός")])
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

def duty_query():
    return Duty_types.query.all()

class AddDutyForm(FlaskForm):
    lastname = QuerySelectField("Ονοματεπώνυμο",
            query_factory = user_query, get_label=lambda user:
            user.lastname + " " + user.name)
    duty_type = QuerySelectField("Τύπος υπηρεσίας", query_factory = duty_query,
            get_label=lambda duty: duty.name)
    duty_date = DateField("Ημερομηνία", format="%Y-%m-%d")
    submit = SubmitField("Προσθήκη")

class EditDutyForm(FlaskForm):
    lastname = QuerySelectField("Ονοματεπώνυμο", query_factory = user_query,
            get_label=lambda user: user.lastname + " " + user.name)
    duty_type = QuerySelectField("Τύπος υπηρεσίας", query_factory = duty_query,
            get_label=lambda duty: duty.name)
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
    lastname = QuerySelectField("Ονοματεπώνυμο", query_factory = user_query, get_label=lambda user:
            user.lastname + " " + user.name)
    add = SubmitField("Προσθήκη στη λίστα")
    clear = SubmitField("Καθαρισμός λίστας")
    duty_type = QuerySelectField("Τύπος υπηρεσίας", query_factory = duty_query,
            get_label=lambda duty: duty.name)
    date_options = SelectField("Επιλογές", choices=[("week","Εβδομάδα"),
        ("month", "Μήνας")])
    submit = SubmitField("Αυτόματη παραγωγή")

class AddNewDutyType(FlaskForm):
    name = StringField("Ονομασία υπηρεσίας",
            validators=[DataRequired()],
            render_kw={"placeholder": "Ονομασία υπηρεσίας"})
    submit = SubmitField("Προσθήκη")

class EditDutyType(FlaskForm):
    name = StringField("Όνομα",validators=[DataRequired()])
    submit = SubmitField("Αποθήκευση αλλαγών")

class AddAbsentTypeForm(FlaskForm):
    name = StringField("Ονομασία άδειας", validators=[DataRequired()],
            render_kw={"placeholder": "Ονομασία άδειας"})
    submit = SubmitField("Προσθήκη")

def absent_types_query():
    return Absent_types.query.all()

class AddAbsentForm(FlaskForm):
    lastname = QuerySelectField("Ονοματεπώνυμο", query_factory = user_query,
            get_label=lambda user: user.lastname + " " + user.name)
    absent_type = QuerySelectField("Τύπος άδειας",
            query_factory = absent_types_query,
            get_label=lambda absent_type: absent_type.name)
    start = DateField("Ημερομηνία: Αρχή άδειας", format="%Y-%m-%d")
    end = DateField("Ημερομηνία: Τέλος άδειας", format="%Y-%m-%d")
    days = IntegerField("Ημέρες")
    submit = SubmitField("Καταχώρηση άδειας")

class EditAbsentForm(FlaskForm):
    lastname = QuerySelectField("Ονοματεπώνυμο", query_factory = user_query,
            get_label=lambda user: user.lastname + " " + user.name)
    absent_type = QuerySelectField("Τύπος άδειας",
            query_factory = absent_types_query,
            get_label=lambda absent_type: absent_type.name)
    days = IntegerField()
    start = DateField("Ημερομηνία: Αρχή άδειας", format="%Y-%m-%d")
    end = DateField("Ημερομηνία: Τέλος άδειας", format="%Y-%m-%d")
    submit = SubmitField("Καταχώρηση άδειας")

class EditAbsentTypeForm(FlaskForm):
    name = StringField("Ονομασία άδειας", validators=[DataRequired()],
            render_kw={"placeholder": "Ονομασία άδειας"})
    submit = SubmitField("Αποθήκευση αλλαγών")

class UpdateAdminPasswordForm(FlaskForm):
    password = PasswordField("Κωδικός", validators=[DataRequired()])
    confirm = PasswordField("Επαλήθευση κωδικού",
            validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("submit")
