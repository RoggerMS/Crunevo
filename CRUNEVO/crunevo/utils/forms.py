# utils/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField(
        'Correo',
        validators=[
            DataRequired(message='El correo es obligatorio.'),
            Email(message='Introduce un correo válido.')
        ],
        render_kw={"placeholder": "Correo electrónico", "class": "form-input"}
    )

    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message='La contraseña es obligatoria.')],
        render_kw={"placeholder": "Contraseña", "class": "form-input"}
    )

    submit = SubmitField('Iniciar sesión', render_kw={"class": "btn btn-primary"})


class RegisterForm(FlaskForm):
    username = StringField(
        'Nombre de usuario',
        validators=[
            DataRequired(message='El nombre de usuario es obligatorio.'),
            Length(min=3, max=20, message='Debe tener entre 3 y 20 caracteres.')
        ],
        render_kw={"placeholder": "Ej. rogger_22", "class": "form-input"}
    )

    email = StringField(
        'Correo electrónico',
        validators=[
            DataRequired(message='El correo es obligatorio.'),
            Email(message='Introduce un correo válido.')
        ],
        render_kw={"placeholder": "Ej. nombre@email.com", "class": "form-input"}
    )

    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message='La contraseña es obligatoria.')],
        render_kw={"placeholder": "********", "class": "form-input"}
    )

    confirm_password = PasswordField(
        'Confirmar contraseña',
        validators=[
            DataRequired(message='Debes confirmar tu contraseña.'),
            EqualTo('password', message='Las contraseñas no coinciden.')
        ],
        render_kw={"placeholder": "Repite la contraseña", "class": "form-input"}
    )

    submit = SubmitField('Registrarse', render_kw={"class": "btn btn-primary"})
