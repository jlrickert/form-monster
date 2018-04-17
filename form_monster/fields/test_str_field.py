import pytest

from . import StrField
from ..exc import ValueErr


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
    return StrField(
        "Full Name",
        dependencies=[first_name, last_name],
        compute=lambda first, last: first + " " + (last or ""))



class TestValueSetting():
    def test_setting_computed(self, full_name):
        assert full_name.is_valid() is False
        last = full_name.get_value()
        full_name.set_value("rawr")
        assert full_name.get_value() == last

    def test_valid_computed(self, first_name, last_name, full_name):
        first_name.set_value("Aaron")
        last_name.set_value("Abraham")
        assert full_name.get_value() == "Aaron Abraham"

    def test_set_value(self, first_name):
        assert first_name.get_value() == None

        first_name.set_value("Jack")
        assert first_name.get_value() == "Jack"


class TestValidation():
    def test_defaults(self, first_name, last_name, signature, full_name):
        assert first_name.is_valid() is False
        assert last_name.is_valid() is True
        assert signature.is_valid() is False
        assert full_name.is_valid() is False

    def test_optional(self, first_name, last_name):
        assert first_name.is_valid() is False
        first_name.set_value("")
        assert first_name.is_valid() is True
        assert last_name.is_valid() is True

    def test_computed(self, first_name, last_name, full_name):
        assert full_name.is_valid() is False

        last_name.set_value("Rabbit")
        assert full_name.is_valid() is False

        first_name.set_value("Jack")
        assert full_name.is_valid() is True

        last_name.set_value(None)
        assert full_name.is_valid() is True

    def test_custom_validate(self, signature):
        assert signature.is_valid() is False

        signature.set_value("jacob")
        assert signature.is_valid() is False

        signature.set_value("Jack")
        assert signature.is_valid() is True
