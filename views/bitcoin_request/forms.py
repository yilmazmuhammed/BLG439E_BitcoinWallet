from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, FloatField
from wtforms.validators import InputRequired, NumberRange

from views.utilities.forms import form_open, form_close


class RequestBitcoinForm(FlaskForm):
    open = form_open(form_name="request-bitcoin-form", f_id="request-bitcoin-form")
    close = form_close()

    amount = FloatField(
        "Amount:",
        validators=[
            InputRequired(message="Please enter amount. If you want it to be ignored, please enter 0 "),
            NumberRange(min=0, message="Please enter amount greater than or equal to 0")
        ],
        id="amount", render_kw={"placeholder": "Amount", "class": "form-control"}
    )

    min_amount = FloatField(
        "Minimum transfer amount to be received:",
        validators=[
            InputRequired(message="Please enter minimum amount. If you want it to be ignored, please enter 0 "),
            NumberRange(min=0, message="Please enter minimum amount greater than or equal to 0")
        ],
        id="min_amount", render_kw={"placeholder": "Minimum amount", "class": "form-control"}
    )

    max_total = FloatField(
        "Maximum amount to be received in total:",
        validators=[
            InputRequired(message="Please enter maximum amount in total. If you want it to be ignored, please enter 0 "),
            NumberRange(min=0, message="Please enter maximum amount in total greater than or equal to 0")
        ],
        id="max_total", render_kw={"placeholder": "Maximum amount in total", "class": "form-control"}
    )

    max_count = IntegerField(
        "Maximum number of transfers to be received:",
        validators=[
            InputRequired(message="Please enter maximum count. If you want it to be ignored, please enter 0 "),
            NumberRange(min=0, message="Please enter maximum count greater than or equal to 0")
        ],
        id="max_count", render_kw={"placeholder": "Maximum count", "class": "form-control"}
    )

    submit = SubmitField(label="Send", render_kw={"class": "btn-color"})


def create_number_range_validator(field_name=None, min_number=None, max_number=None):
    field_name = field_name if field_name else "number"
    if min_number and max_number:
        range_string = "between %s and %s" % (min_number, max_number,)
    elif min_number:
        range_string = "greater than %s" % (min_number,)
    else:
        range_string = "smaller than %s" % (max_number,)
    message = "Please enter %s must be %s" % (field_name, range_string)
    return NumberRange(min=min_number, message=message)
