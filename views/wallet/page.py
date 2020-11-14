from flask import render_template, g
from flask_login import current_user

from views.transfer.db import db_get_my_transfers
from views.utilities import LayoutPI


def my_wallet_page():
    g.transfers = db_get_my_transfers(current_user.wallet_ref.id)
    return render_template("wallet/my_wallet.html", page_info=LayoutPI(title="Welcome"))
