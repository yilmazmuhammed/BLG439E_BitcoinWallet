from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import InputRequired

from views.utilities.forms import form_open, form_close


class SendBitcoinForm(FlaskForm):
    open = form_open(form_name="send-bitcoin-form", f_id="send-bitcoin-form")
    close = form_close()

    receiver_address = StringField(
        "Receiver address:",
        validators=[
            InputRequired("Please enter receiver wallet address"),
            # Length(max=40, message="Receiver wallet address cannot be longer 40 characters.")
        ],
        id='receiver_address', render_kw={"placeholder": "Receiver address"}
    )

    amount = DecimalField(
        "Amount:",
        validators=[
            InputRequired("Please enter amount")
        ],
        id="amount", render_kw={"placeholder": "Amount"}
    )

    submit = SubmitField(label="Send", render_kw={"class": "btn-color"})