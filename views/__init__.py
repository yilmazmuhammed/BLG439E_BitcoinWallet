from flask import render_template, redirect, url_for
from flask_login import current_user

from views.utilities import LayoutPI


def home_page():
    if current_user.is_authenticated:
        return redirect(url_for("my_wallet_page"))
    else:
        return redirect(url_for("login_page"))
