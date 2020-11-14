from copy import copy

from bit.exceptions import InsufficientFunds
from flask import render_template, url_for, g, flash, abort
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from views.bitcoin_request.db import db_add_bitcoin_request, db_get_bitcoin_request
from views.bitcoin_request.forms import RequestBitcoinForm
from views.transfer.db import db_send_bitcoin
from views.utilities import FormPI, LayoutPI
from views.wallet.forms import SendBitcoinForm


@login_required
def new_bitcoin_request_page():
    form = RequestBitcoinForm()

    if form.validate_on_submit():
        if form.amount.data and form.amount.data < 0:
            flash("Please enter maximum count greater than 0 or not enter value", "error")
        elif form.min_amount.data and form.min_amount.data < 0:
            flash("Please enter maximum count greater than 0 or not enter value", "error")
        elif form.max_count.data and form.max_count.data < 0:
            flash("Please enter maximum count greater than 0 or not enter value", "error")
        elif form.max_total.data and form.max_total.data < 0:
            flash("Please enter maximum count greater than 0 or not enter value", "error")
        else:
            db_add_bitcoin_request(
                wallet_ref=current_user.wallet_ref,
                amount=form.amount.data,
                min_amount=form.min_amount.data,
                max_count=form.max_count.data,
                max_total=form.max_total.data,
            )
            return redirect(url_for("my_bitcoin_requests_page"))

    return render_template("form.html", page_info=FormPI(form=form, title="Request Bitcoin"))


def my_bitcoin_requests_page():
    my_bitcoin_requests = current_user.wallet_ref.bitcoin_requests_set.select()[:]
    g.my_bitcoin_requests = my_bitcoin_requests
    return render_template("bitcoin_request/my_bitcoin_requests.html", page_info=LayoutPI(title="My Bitcoin Requests"))


def bitcoin_request_page(bitcoin_request_id):
    bitcoin_request = db_get_bitcoin_request(bitcoin_request_id)
    if not bitcoin_request:
        abort(404)
    if bitcoin_request.wallet_ref.web_user_ref.id == current_user.id:
        g.bitcoin_request = bitcoin_request
        return render_template("bitcoin_request/bitcoin_request_information.html",
                               page_info=LayoutPI(title="My Bitcoin Requests"))
    else:
        g.bitcoin_request = bitcoin_request
        if not bitcoin_request.is_active:
            flash("This bitcoin request is not active.", "info")
            return render_template("layout.html", page_info=LayoutPI(title="Send Bitcoin to Request"))
        elif ((bitcoin_request.max_count and bitcoin_request.max_count < bitcoin_request.transfers_set.count())
              or bitcoin_request.remaining_amount_from_total) == 0:
            flash("This request received bitcoins that are enough amount or enough count.", "info")
            return render_template("layout.html", page_info=LayoutPI(title="Send Bitcoin to Request"))

        form = SendBitcoinForm()
        form.__delitem__("receiver_address")
        min_amount = max_amount = None
        if bitcoin_request.min_amount or bitcoin_request.max_total:
            min_amount = bitcoin_request.min_amount
            max_amount = bitcoin_request.remaining_amount_from_total
        if bitcoin_request.amount:
            form.amount.data = bitcoin_request.amount
            form.amount.render_kw["readonly"] = ""
            min_amount = max_amount = bitcoin_request.amount
        print(form.amount.data)
        print(form.amount.errors)
        for i in form:
            print(i.errors)
        if form.validate_on_submit():
            print("asd")
            if (min_amount and form.amount.data < min_amount) or (max_amount and form.amount.data > max_amount):
                flash("Amount must be between %s and %s" % (min_amount, max_amount), "error")
            else:
                form.amount.render_kw.pop("readonly")
                try:
                    db_send_bitcoin(
                        sender_wallet=current_user.wallet_ref,
                        amount=form.amount.data,
                        bitcoin_request_ref=bitcoin_request
                    )
                except InsufficientFunds as e:
                    flash(str(e), "danger")
                return redirect(url_for("my_wallet_page"))
        return render_template("form.html", page_info=FormPI(form=form, title="Send Bitcoin to Request"))