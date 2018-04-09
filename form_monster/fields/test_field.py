import pytest
import re

from .field import Field


def computeTotalLegs(cat_count, dog_count):
    s = 0
    if cat_count is not None:
        s = s + cat_count
    if dog_count is not None:
        s = s + dog_count
    return s * 4


@pytest.fixture
def minimal_field():
    return Field(
        'example_field', options={
            "text": "Example",
        })


@pytest.fixture
def cost_range_field():
    return Field(
        'prepay',
        options={
            "text": "Prepay amount",
            "type": float,
            "validate": lambda x: 10.0 <= x <= 20.0,
            "error_msg": lambda x: "%s in not between 10 and 20",
            "nullable": False,
        })


@pytest.fixture
def compute_form():
    forms = {
        "cat_count":
        Field("cat_count", options={
            "text": "Number of cats",
            "type": int,
        }),
        "dog_count":
        Field("dog_count", options={
            "text": "Number of dogs",
            "type": int,
        })
    }
    forms["total_legs"] = Field(
        "total_legs",
        dependencies=[
            forms.get("dog_count"),
            forms.get("cat_count"),
        ],
        options={
            "text": "Total legs",
            "type": int,
            "compute": computeTotalLegs,
        })
    return forms


class TestMinimumField(object):
    def test_name(self, minimal_field):
        assert minimal_field.name == "example_field"

    def test_text(self, minimal_field):
        assert minimal_field.text == "Example"

    def test_value(self, minimal_field):
        assert minimal_field.value is None

        minimal_field.value = "Jack"
        assert minimal_field.value == "Jack"

    def test_default_is_valid(self, minimal_field):
        assert minimal_field.is_valid() is True
        minimal_field.value = "5"
        assert minimal_field.is_valid() is True

    def test_error_msg(self, minimal_field):
        msg = minimal_field.error_msg()
        assert re.findall(r"missing", msg) == ["missing"]

        minimal_field.value = "5"
        msg = minimal_field.error_msg()
        assert re.findall(r"invalid", msg) == ["invalid"]


class TestField(object):
    def test_name(self, cost_range_field):
        assert cost_range_field.name == "prepay"

    def test_text(self, cost_range_field):
        assert cost_range_field.text == "Prepay amount"

    def test_value(self, cost_range_field):
        assert cost_range_field.value is None

        cost_range_field.value = "12"
        assert cost_range_field.value == 12

    def test_validation(self, cost_range_field):
        cost_range_field.value = "5.4"
        assert cost_range_field.is_valid() is False

        cost_range_field.value = "12.0"
        assert cost_range_field.is_valid() is True

        cost_range_field.value = "21.3"
        assert cost_range_field.is_valid() is False

    def test_error_msg(self, cost_range_field):
        msg = cost_range_field.error_msg()
        assert re.findall(r"missing", msg) == ["missing"]

        cost_range_field.value = "5"
        msg = cost_range_field.error_msg()
        assert re.findall(r"between", msg) == ["between"]


def test_compute(compute_form):
    cat_count = compute_form.get("cat_count")
    dog_count = compute_form.get("dog_count")
    total_legs = compute_form.get("total_legs")
    cat_count.value = "5"
    assert cat_count.value == 5
    assert total_legs.value == 5 * 4

    dog_count.value = "10"
    assert dog_count.value == 10
    assert total_legs.value == 15 * 4
