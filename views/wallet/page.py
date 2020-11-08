from flask import render_template

from views.utilities import LayoutPI


def my_wallet_page():
    return render_template("wallet/my_wallet.html", page_info=LayoutPI(title="Welcome"))
