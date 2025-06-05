from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    email = StringField("Correo Electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember_me = BooleanField("Recordarme")
    submit = SubmitField("Iniciar Sesión")

class RegisterForm(FlaskForm):
    name = StringField("Nombre Completo", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Correo Electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar Contraseña", validators=[DataRequired(), EqualTo("password")])
    faculty = SelectField("Facultad", choices=[
        ("", "Selecciona tu facultad"),
        ("Ciencias", "Ciencias"),
        ("Humanidades", "Humanidades"),
        ("Ingenieria", "Ingeniería"),
        ("Educacion", "Educación"),
        ("Agropecuaria y Nutrición", "Agropecuaria y Nutrición"),
        ("Tecnología", "Tecnología"),
        ("Ciencias Empresariales", "Ciencias Empresariales")
    ], validators=[Optional()])
    career = StringField("Carrera", validators=[Optional(), Length(max=100)])
    study_year = SelectField("Año de Estudio", choices=[
        ("", "Selecciona tu año"),
        ("1", "1er Año"),
        ("2", "2do Año"),
        ("3", "3er Año"),
        ("4", "4to Año"),
        ("5", "5to Año"),
        ("egresado", "Egresado"),
        ("otro", "Otro")
    ], validators=[Optional()])
    profile_picture = FileField("Foto de Perfil", validators=[Optional()]) # Validator for file type can be added
    submit = SubmitField("Crear Cuenta")

