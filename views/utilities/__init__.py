from werkzeug.datastructures import MultiDict


def flask_form_to_dict(request_form: MultiDict, exclude=[]):
    result = {
        key: request_form.getlist(key)[0] if len(request_form.getlist(key)) == 1 else request_form.getlist(key)
        for key in request_form
    }

    result2 = {}
    for key in result:
        if not result[key] == "" and key not in exclude:
            result2[key] = result[key]
        # else:
        #     print("Message 1: Boş string pop'landı. key =", key, "->", result[key], "(views/yardimci.py)")

    result2.pop('submit', None)
    result2.pop('csrf_token', None)

    return result2


class LayoutPI:
    def __init__(self, title):
        self.title = title
        self.website_name = "WeeWallet"


class FormPI(LayoutPI):
    def __init__(self, form, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = form
        self.errors = []
        for field in form:
            self.errors += field.errors