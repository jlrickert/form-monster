from collections import OrderedDict
from datetime import date, datetime, timedelta

import pytest

from .form import Form
from .fields import StrField, DateField, BoolField

days_in_year = int(18.0 * 365.25)


def compute_over_18(birth_date):
    if birth_date:
        return (datetime.now().date() - birth_date).days >= days_in_year


@pytest.fixture
def first_name():
    return StrField("First Name")


@pytest.fixture
def last_name():
    return StrField("Last Name", optional=True)


@pytest.fixture
def signature():
    return StrField("Signature", validate=lambda name: name == "Jack")


@pytest.fixture
def full_name(first_name, last_name):
    print("computing", first_name, last_name)
    return StrField(
        "Full Name",
        dependencies=[first_name, last_name],
        compute=lambda first, last: (first or "") + " " + (last or ""))


@pytest.fixture
def date_of_birth():
    return DateField("Date of Birth")


@pytest.fixture
def over_18(date_of_birth):
    return BoolField(
        "Over 18", dependencies=[date_of_birth], compute=compute_over_18)


@pytest.fixture
def example_form(first_name, last_name, signature, full_name, date_of_birth,
                 over_18):
    print('asds')
    form = Form(
        fields={
            "first_name": first_name,
            "last_name": last_name,
            "signature": signature,
            "full_name": full_name,
            "date_of_birth": date_of_birth,
            "over_18": over_18
        })
    print('gasdfe')
    return form

def compute_full_name(first_name, last_name):
    first = first_name or ""
    last = ""
    if last_name:
        last = (" " + last_name)
    return first + last


@pytest.fixture
def self_contained_form():
    form = Form(
        fields={
            "first_name": StrField("First Name"),
            "last_name": StrField("Last Name", optional=True),
            "signature": StrField("signature", validate=lambda name: name == "Jack"),
            "full_name": StrField(
                "Full Name",
                dependencies=["first_name", "last_name"],
                compute=compute_full_name),
            "date_of_birth": DateField("Date of Birth"),
            "over_18": BoolField(
                "Over 18",
                dependencies=["date_of_birth"],
                compute=compute_over_18)
        })
    return form


@pytest.fixture
def forms(example_form, self_contained_form):
    return [example_form, self_contained_form]


class TestValues():
    def test_set_value_for_simple_form(self, forms):
        for form in forms:
            form.set_value("first_name", "jack")
            assert form.get_value("first_name") == "jack"

    def test_computed(self, full_name, forms):
        for form in forms:
            assert id(full_name) != id(form.get_field("full_name"))
            form.set_value("first_name", "Jack")
            form.set_value("last_name", "Rabbit")
            assert form.get_value("full_name") == "Jack Rabbit"


class TestValidation():
    def test_invalid_from_optional_fields(self, forms):
        for form in forms:
            assert form.is_valid() is False

    def test_invalid(self, forms):
        for form in forms:
            form.set_value("first_name", "Jack")
            form.set_value("signature", "Rawr")
            assert form.is_valid() is False

    def test_valid(self, forms):
        for form in forms:
            form.set_value("first_name", "Jack")
            form.set_value("signature", "Jack")
            dob = (datetime.now() - timedelta(days=(5 + 22 * 365))).date()
            form.set_value("date_of_birth", dob)

            for k, field in form.get_fields():
                if not field.is_valid():
                    print(k, repr(field), field.get_value())
                assert field.is_valid() is True

            assert form.is_valid() is True
