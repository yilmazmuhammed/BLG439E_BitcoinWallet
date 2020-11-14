from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from views.transfer.db import db_send_bitcoin
from views.utilities import FormPI
from views.wallet.forms import SendBitcoinForm


@login_required
def send_bitcoin_page():
    form = SendBitcoinForm()

    if form.validate_on_submit():
        db_send_bitcoin(
            sender_wallet=current_user.wallet_ref,
            receiver_address=form.receiver_address.data,
            amount=form.amount.data
        )
        print(form.receiver_address.data)
        print(form.amount.data)
        return redirect(url_for("my_wallet_page"))

    form.receiver_address.data = request.args.get("receiver")
    return render_template("form.html", page_info=FormPI(form=form, title="Send Bitcoin"))
