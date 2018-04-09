import pytest

from . import StrField
from ..exc import ValueErr


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


def test_set_value(first_name):
    assert first_name.get_value() == None

    first_name.set_value("Jack")
    assert first_name.get_value() == "Jack"


class TestValidation():
    def test_defaults(self, first_name):
        assert first_name.is_valid() is True

    def test_optional(self, last_name):
        assert last_name.is_valid() is False
        last_name.set_value("")
        assert last_name.is_valid() is True

    def test_custom_validate(self, signature):
        assert signature.is_valid() is False

        signature.set_value("jacob")
        assert signature.is_valid() is False

        signature.set_value("Jack")
        assert signature.is_valid() is True


class TestComputed():
    def test_invalid(self, full_name):
        assert full_name.is_valid() is True
        last = full_name.get_value()
        full_name.set_value("rawr")
        assert full_name.get_value() == last
