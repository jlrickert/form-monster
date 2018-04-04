import pytest

from form_monster.field import Field


def computeTotalLegs(cat_count, dog_count):
    s = 0
    if cat_count is not None:
        s = s + cat_count
    if dog_count is not None:
        s = s + dog_count
    return s * 4


@pytest.fixture
def computeForm():
    form = {}
    cat_count = Field(
        "cat_count",
        form=form,
        options={
            "text": "Number of cats",
            "type": int,
        })
    dog_count = Field(
        "dog_count",
        form=form,
        options={
            "text": "Number of dogs",
            "type": int,
        })
    total_legs = Field(
        "total_legs",
        form=form,
        options={
            "text": "Total legs",
            "type": int,
            "compute": computeTotalLegs,
        })
    form[dog_count.name] = dog_count
    form[cat_count.name] = cat_count
    form[total_legs.name] = total_legs
    return form


class TestMinimumField(object):
    field = Field(
        'example_field', options={
            "text": "Example",
        })

    def test_name(self):
        assert self.field.name == "example_field"

    def test_text(self):
        assert self.field.text == "Example"

    def test_value(self):
        assert self.field.value is None

        self.field.value = "Jack"
        assert self.field.value == "Jack"

    def test_error_msg(self):
        pass


class TestComplexField(object):
    pass


def test_compute(computeForm):
    cat_count = computeForm.get("cat_count")
    dog_count = computeForm.get("dog_count")
    total_legs = computeForm.get("total_legs")
    cat_count.value = "5"
    assert cat_count.value == 5
    assert total_legs.value == 5 * 4

    dog_count.value = "10"
    assert dog_count.value == 10
    assert total_legs.value == 15 * 4
