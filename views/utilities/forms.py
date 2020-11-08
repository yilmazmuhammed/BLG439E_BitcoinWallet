def form_open(form_name, f_id=None, enctype=None, f_action=""):
    f_open = """<form action="%s" method="post" name="%s" """ % (f_action, form_name,)

    if f_id:
        f_open += """ id="%s" """ % (f_id,)
    if enctype:
        f_open += """ enctype="%s" """ % (enctype,)

    f_open += """class="main-form full">"""

    return f_open


def form_close():
    return """</form>"""
