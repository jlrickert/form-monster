import logging
from datetime import datetime, date
from form_monster import Form, Web, WxView

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

def compute_over_18(date_of_birth):
    if date_of_birth:
        return (date.today() - date_of_birth).days >= 18 * 365.25

form = Form({
    "first_text": StrField("First Name"),
    "last_text": StrField("Last Name", options={
        "error_msg": "{value} is invalid for field {field}"
    }),

    "date_of_birth": DateField("Date of Birth", options={
        "optional": False,
        "validate": lambda x: x <= datetime.now().date()
    }),

    "over_18": BoolField("Over 18", dependencies=["date_of_birth"], options={
        "compute": compute_over_18,
    })
})

view = WxView(form)
data = view.run()
print(data)
