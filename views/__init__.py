from flask import render_template
from flask_login import current_user

from views.utilities import LayoutPI


def home_page():
    if current_user.is_authenticated:
        print("---home page---")
        print(current_user.wallet_ref.key)
        print(current_user.wallet_ref.key.address)
        print(current_user.wallet_ref.wallet_address)
        return render_template("layout.html", page_info=LayoutPI(title="Hello %s" % current_user.username))
    else:
        return render_template("layout.html", page_info=LayoutPI(title="Welcome"))