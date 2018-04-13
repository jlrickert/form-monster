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
    return StrField("First Name", optional=False)


@pytest.fixture
def last_name():
    return StrField("Last Name")


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


@pytest.fixture
def date_of_birth():
    return DateField("Date of Birth")


@pytest.fixture
def over_18(date_of_birth):
    return DateField(
        "Over 18", dependencies=[date_of_birth], compute=compute_over_18)


@pytest.fixture
def example_form(first_name, last_name, signature, full_name, date_of_birth,
                 over_18):
    form = Form()
    form.add_fields(
        [first_name, last_name, signature, full_name, date_of_birth, over_18])
    return form


class TestValidation():
    def test_invalid(self, first_name, signature, example_form):
        assert example_form.is_valid() is False
        first_name.set_value("Jack")
        signature.set_value("Rawr")
        assert example_form.is_valid() is False

    def test_valid(self, first_name, signature, example_form):
        first_name.set_value("Jack")
        signature.set_value("Jack")
        assert example_form.is_valid() is True
