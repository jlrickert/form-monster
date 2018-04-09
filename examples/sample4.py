import logging
from datetime import datetime, date
from form_monster import Form, Web, WxView

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


def valid_date(value):
    return value <= datetime.now().date()


def compute_over_18(date_of_birth):
    if date_of_birth:
        return (date.today() - date_of_birth).days >= 18 * 365.25


def compute_full_name(first_name, last_name):
    return "{first} {last}".format(first_name, last_name)

form = FormMonster()\
       .add_field("first_name", field=StrField("First Name"))\
       .add_field("last_name", field=StrField("Last Name"))\
       .add_field("county", field=StrField("county", choices=["county a", "county b", "county b"]))\
       .add_field("full_name",
                  field=StrField(
                      "Last Name",
                      compute=compute_full_name), optional=True)\
       .add_field("date_of_birth", DateField("Date of Birth", validate=valid_date))\
       .add_field("over_18", BoolField("Date of Birth", compute=compute_over_18))

form.set_field("date_of_birth")
# form = Form({
#     "first_text": StrField("First Name"),
#     "last_text": StrField("Last Name", options={
#         "error_msg": "{value} is invalid for field {field}"
#     }),

#     "date_of_birth": DateField("Date of Birth", options={
#         "optional": False,
#         "validate": lambda x: x <= datetime.now().date()
#     }),

#     "over_18": BoolField("Over 18", dependencies=["date_of_birth"], options={
#         "compute": compute_over_18,
#     })
# })

view = WxView(form)
data = view.run()
print(data)
