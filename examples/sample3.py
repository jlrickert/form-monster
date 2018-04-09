import logging
from datetime import datetime, date
from form_monster import Form, Web, WxView

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


class Field():
    pass


class ComputedField(Field):
    pass


class FirstName(Field):
    text = "First Name"


class LastName(Field):
    text = "Last Name"
    error_message = "%s is invalid for field"


class FullName(ComputedField):
    text = "Full name"

    def compute(self, deps):
        pass


class BirthDate(Field):
    text = "Date of Birth"


class Over18(ComputedField):
    text = "Over 18"
    dependencies = [BirthDate]

    def compute(self):
        date_of_birth = deps.get("date_of_birth")
        if deps[0]:
            return (date.today() - date)


def compute_over_18(date_of_birth):
    if date_of_birth:
        return (date.today() - date_of_birth).days >= 18 * 365.25


form = Form({
    "first_text": FirstName,
    "last_text": LastName,
    "date_of_birth": DateField,
    "over_18": Over18({
        "dob": "date_of_birth"
    }),
})

view = WxView(form)
data = view.run()
print(data)
