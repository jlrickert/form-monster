import logging
from datetime import datetime, date
from form_monster import Form, Web, WxView
from form_monster.fields import StrField, DateField, BoolField

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

def maxis_save(x):
    pass


def valid_date(value):
    return value <= datetime.now().date()


def compute_over_18(date_of_birth):
    if date_of_birth:
        return (date.today() - date_of_birth).days >= 18 * 365.25


def compute_full_name(first_name, last_name):
    return "{first} {last}".format(first_name, last_name)


first_name = StrField("First Name", optional=False, value="jff")   # this line
last_name = StrField("Last Name", value="Rabbit")
full_name = StrField(
    "Full Name",
    dependencies=[first_name, last_name],
    computed=compute_full_name)
date_of_birth = DateField("Date of Birth")
over_18 = BoolField(
    "Over 18", dependencies=[date_of_birth], computed=compute_over_18)

form = Form()
form.add_fields([first_name, last_name, full_name, date_of_birth, over_18])
view = WxView(form)                                 # does mutations
data = view.run()


# first_name is jeff
data["first_name"] is "jeff"
first_name.get_value()                             # this line here

maxis_save(data)

print(data)
