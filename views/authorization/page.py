from flask import flash, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
from passlib.handlers.pbkdf2 import pbkdf2_sha256 as hasher

from views.authorization.db import db_add_web_user, get_web_user
from views.authorization.forms import RegisterForm, LoginForm
from views.exceptions import RegisterException
from views.utilities import flask_form_to_dict, FormPI


def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_verification.data:
            flash(u"if block: Passwords do not match", 'danger')
        else:
            try:
                json_data = flask_form_to_dict(request_form=request.form, exclude=['password_verification'])
                db_add_web_user(json_web_user=json_data)
                flash("Web user created.", 'success')
                return redirect(url_for('login_page'))
            except RegisterException as ex:
                flash(u"%s" % ex, 'danger')

    return render_template("form.html", page_info=FormPI(form=form, title="Register"))


def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        user = get_web_user(username=form.username.data)
        if user and hasher.verify(form.password.data, user.password_hash) and user.is_active:
            login_user(user)
            flash("Login successful", 'success')
            next_page = request.args.get("next", url_for("home_page"))
            return redirect(next_page)
        else:  # If password or username is incorrect
            flash("Password or email is wrong", 'danger')
    return render_template("form.html", page_info=FormPI(form=form, title="Login Page"))


@login_required
def logout_page():
    logout_user()
    flash(u"Logout", 'success')
    return redirect(url_for("home_page"))
