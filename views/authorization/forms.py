from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo

from views.utilities.forms import form_open, form_close


class RegisterForm(FlaskForm):
    # first_name = StringField(
    #     "%s:" % t['first_name']['label'],
    #     validators=[InputRequired(t['first_name']['required']), Length(max=40, message=t['first_name']['length'])],
    #     id='first_name', render_kw={"placeholder": t['first_name']['label']}
    # )
    #
    # last_name = StringField(
    #     "%s:" % t['last_name']['label'],
    #     validators=[InputRequired(t['last_name']['required']), Length(max=40, message=t['last_name']['length'])],
    #     id='last_name', render_kw={"placeholder": t['last_name']['label']}
    # )
    open = form_open(form_name="register-form", f_id="register-form")
    close = form_close()
    username = StringField(
        "Username:",
        validators=[InputRequired("Please enter your username"),
                    Length(max=40, message="Username cannot be longer 40 characters.")],
        id='username', render_kw={"placeholder": "Username"}
    )

    email = EmailField(
        "Email:",
        validators=[
            InputRequired("Please enter your email"),
            Length(max=254, message="Email cannot be longer than 54 characters."),
            Email("Please enter valid email")
        ],
        id='email', render_kw={"placeholder": "Email"}
    )

    # phone_number = TelField(
    #     "%s:" % t['phone_number']['label'],
    #     validators=[Length(max=20, message=t['phone_number']['length'])],
    #     id='phone_number', render_kw={"placeholder": t['phone_number']['label']}
    # )

    password = PasswordField(
        "Password:",
        validators=[InputRequired("Please enter your password"),
                    Length(max=30, message="Password cannot be longer than 30 characters")],
        id='password', render_kw={"placeholder": "Password"}
    )

    password_verification = PasswordField(
        "Password verification:",
        validators=[InputRequired("Please enter your password verification"),
                    Length(max=30, message="Password verification cannot be longer than 30 characters"),
                    EqualTo('password', message="Passwords do not match")],
        id='password_verification', render_kw={"placeholder": "Password verification"}
    )

    # is_admin = BooleanField(
    #     label="%s:" % t['is_admin']['label'], id='is_admin',
    #     render_kw={"class": "checkbox"}
    # )
    #
    # is_active = BooleanField(
    #     label="%s:" % t['is_active']['label'], id='is_active',
    #     render_kw={"data-toggle": "toggle", "data-onstyle": "success"}
    # )

    submit = SubmitField(label="Submit", render_kw={"class": "btn-color"})


class LoginForm(FlaskForm):
    open = form_open(form_name='form-login')
    close = form_close()
    form_title = "Login Form"

    username = StringField(
        "Username:",
        validators=[InputRequired("Please enter your username"),
                    Length(max=40, message="Username cannot be longer 40 characters.")],
        id='last_name', render_kw={"placeholder": "Username"}
    )

    password = PasswordField(
        "Password:",
        validators=[InputRequired("Please enter your password"),
                    Length(max=30, message="Password cannot be longer than 30 characters")],
        id='password', render_kw={"placeholder": "Password"}
    )

    submit = SubmitField(label="Submit", render_kw={"class": "btn-color"})
