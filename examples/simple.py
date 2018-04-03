from datetime import datetime, date
from form_monster import Form, Console

form = Form({
    # minimum needed
    'first_name': {
        "name": "First Name",
    },

    # defaults
    'last_name': {
        # name is required
        "name": "Last Name",

        # str is default
        'type': str,                 
        optional: False,
        'validate': lambda x: True,
        'error_msg': lambda value: "%s is invalid for field %s" % value
    },
    'date_of_birth': {
        "name": "Date of Birth",
        "type": date,
        "validate": lambda x: x <= date.now()
    },

    # example calculated value.
    'over_18': {
        "name": "Over 18",
        'type': bool,

        #example that will default to making sure it is a bool
        calculate: lambda dob: (date.now() - dob).years >= 18,

        # Only calculated if all depencies have values. Not required
        depencies: ["date_of_birth"]
    }
})

# view = Console(form)
# view.run()
# print(view.data)
