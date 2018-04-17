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
def expiration_date():
    return DateField("April Fools Date", optional=True)


@pytest.fixture
def over_18(date_of_birth):
    return BoolField("Over 18", dependencies=[date_of_birth], compute=is_over_18)


class TestValidation():
    def test_invalid(self, date_of_birth):
        future = (datetime.now() + timedelta(days=1)).date()
        date_of_birth.set_value(future)
        assert date_of_birth.is_valid() is False

    def test_valid(self, date_of_birth, over_18):
        assert over_18.is_valid() is False
        date_of_birth.set_value("March 24 1992")
        assert date_of_birth.is_valid() is True

        date_of_birth.set_value("19920324")
        assert date_of_birth.is_valid() is True

    def test_optional(self, date_of_birth, expiration_date):
        assert date_of_birth.is_valid() is False
        dob = (datetime.now() - timedelta(days=(5 + 22 * 365))).date()
        date_of_birth.set_value(dob)
        assert date_of_birth.is_valid() is True

        assert expiration_date.is_valid() is True
        expire_date = (datetime.now() + timedelta(days=7)).date()
        expiration_date.set_value(expire_date)
        assert expiration_date.is_valid() is True


class TestValueHandling():
    def test_junk_value(self, date_of_birth):
        try:
            date_of_birth.set_value("rofl")
            assert "Should have thrown an error"
        except ValueErr as e:
            pass

    def test_set_valid_value(self, date_of_birth):
        date_of_birth.set_value("Mar 24 1992")
        value = date_of_birth.get_value()
        assert value == date(1992, 3, 24)

        date_of_birth.set_value("March 24 1992")
        value = date_of_birth.get_value()
        assert value == date(1992, 3, 24)

        date_of_birth.set_value("19920324")
        value = date_of_birth.get_value()
        assert value == date(1992, 3, 24)
