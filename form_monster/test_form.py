from collections import OrderedDict
from datetime import date, datetime

import pytest

from .form import Form
from .fields import StrField, DateField, BoolField

days_in_year = int(18.0 * 365.25)


def compute_over_18(birth_date):
    return (datetime.now().date() - birth_date).days >= days_in_year


@pytest.fixture
def first_name():
    return StrField("First Name")


@pytest.fixture
def last_name():
    return StrField("Last Name", optional=False)


@pytest.fixture
def signature():
    return StrField(
        "Signature", optional=False, validate=lambda name: name == "Jack")


@pytest.fixture
def full_name(first_name, last_name):
    return StrField(
        "Full Name",
        dependencies=[first_name, last_name],
        compute=lambda first, last: (first or "") + " " + (last or ""))
