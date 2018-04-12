from datetime import date, datetime, timedelta

import pytest

from . import DateField, BoolField
from ..exc import ValueErr


@pytest.fixture
def simple_date():
    return DateField("Simple Date")


days_in_year = int(18.0 * 365.25)


def must_be_past(date_):
    if date_ is None:
        return True
    return date_ < datetime.now().date()


def is_over_18(birth_date):
    return (datetime.now().date() - birth_date).days >= days_in_year


@pytest.fixture
def date_of_birth():
    return DateField("Date of Birth", validate=must_be_past)


@pytest.fixture
def over_18(date_of_birth):
    return BoolField("Over 18", dependencies=[over_18], compute=is_over_18)


class TestValidation():
    def test_invalid(self, date_of_birth):
        assert date_of_birth.is_valid() is True

        future = (datetime.now() + timedelta(days=1)).date()
        date_of_birth.set_value(future)
        assert date_of_birth.is_valid() is False

    def test_valid(self, date_of_birth):
        assert date_of_birth.is_valid() is True


class TestValueHandling():
    def test_junk_value(self, date_of_birth):
        try:
            date_of_birth.set_value("rofl")
            assert "Should have thrown an error"
        except ValueErr as e:
            assert e is "rawr"
