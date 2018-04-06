import logging
from datetime import datetime, date
from form_monster import Form, Web, WxView

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

def compute_over_18(date_of_birth):
    if date_of_birth:
        return (date.now() - date_of_birth).years >= 18

form = Form({
    # minimum needed
    "first_text": {
        "text": "First Name",
        "optional": False,
    },

    # defaults
    "last_text": {
        # text is required
        "text": "Last Name",

        # str is default
        "type": str,
        "optional": False,
        "validate": lambda x: True,
        "error_msg": lambda value: "%s is invalid for field %s" % value
    },
    'date_of_birth': {
        "text": "Date of Birth",
        "type": date,
        "validate": lambda x: x <= date.now()
    },

    # example calculated value.
    "over_18": {
        "text": "Over 18",
        "type": bool,
        "optional": False,

        # calculates a value when all arguments are valid.
        "compute": compute_over_18,
    }
})

view = WxView(form)
data = view.run()
print(data)
