from collections import OrderedDict
from datetime import date, datetime

import pytest

from form_monster.form import Form

days_in_year = int(18.0 * 365.25)


def compute_over_18(date_of_birth):
    if date_of_birth:
        return (datetime.now().date() - date_of_birth).days >= days_in_year


@pytest.fixture
def form1():
    form = Form(OrderedDict({
        "first_text": {
            "text": "First Name",
            "optional": False,
        },
        "last_text": {
            "text": "Last Name",
            "type": str,
            "optional": False,
            "validate": lambda x: True,
            "error_msg": lambda value: "%s is invalid for field %s" % value
        },
        "date_of_birth": {
            "text": "Date of Birth",
            "type": date,
            "optional": False,
            "validate": lambda x: x <= datetime.now().date()
        },
        "over_18": {
            "text": "Over 18",
            "type": bool,
            "compute": compute_over_18,
        }
    }))
    return form


class TestSimpleform():
    def test_completed_form(self, form1):
        form1.set("first_text", "hello")
        form1.set("last_text", "wassup")
        form1.set("date_of_birth", "19920825")
        assert form1.is_valid()

    def test_incompleted_form(self, form1):
        form1.set("first_text", "hello")
        form1.set("date_of_birth", "19920825")
        assert not form1.is_valid()

    def test_form_order(self, form1):
        names = ["first_text", "last_text", "date_of_birth", "over_18"]
        i = 0
        for key in form1.fields:
            assert names[i] == key
            i += 1
