import pytest

from . import FloatField, IntField
from ..exc import ValueErr


def is_multiple_of_4(*animals):
    s = sum([legs for legs in animals if legs is not None])
    return s % 4 == 0


@pytest.fixture
def dog_legs():
    return IntField("Number of dog legs", optional=True)


@pytest.fixture
def cat_legs():
    return IntField("Number of cat legs")


@pytest.fixture
def cow_legs():
    return IntField("Signature", optional=False, validate=is_multiple_of_4)


@pytest.fixture
def leg_count(dog_legs, cat_legs, cow_legs):
    return IntField(
        "Full Name",
        validate=is_multiple_of_4,
        dependencies=[dog_legs, cat_legs, cow_legs],
        compute=lambda *legs: sum([count for count in legs if count]))


def test_set_value(dog_legs):
    assert dog_legs.get_value() == None

    dog_legs.set_value(4)
    assert dog_legs.get_value() == 4

    dog_legs.set_value("4")
    assert dog_legs.get_value() == 4

    try:
        dog_legs.set_value("BOOM")
        assert "Should throw an error"
    except ValueError:
        pass


class TestValidation():
    def test_defaults(self, dog_legs):
        assert dog_legs.is_valid() is True

    def test_optional(self, cat_legs, dog_legs):
        assert dog_legs.is_valid() is True
        dog_legs.set_value(4)
        assert dog_legs.is_valid() is True

        assert cat_legs.is_valid() is False
        cat_legs.set_value(0)
        assert cat_legs.is_valid() is True

    def test_custom_validate(self, cow_legs):
        cow_legs.set_value(13)
        assert cow_legs.is_valid() is False

        cow_legs.set_value(12)
        assert cow_legs.is_valid() is True


class TestComputed():
    def test_valid(self, dog_legs, cat_legs, cow_legs, leg_count):
        dog_legs.set_value(4)
        cat_legs.set_value(12)
        cow_legs.set_value(24)
        assert leg_count.get_value() == 40

    def test_invalid(self, dog_legs, cat_legs, cow_legs, leg_count):
        dog_legs.set_value(4)
        cat_legs.set_value(5)
        cow_legs.set_value(4)
        assert leg_count.is_valid() is False
