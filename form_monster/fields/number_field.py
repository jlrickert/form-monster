from .base import BaseField

from ..exc import ValueErr


class NumberField(BaseField):
    pass


class IntField(NumberField):
    def set_value(self, value):
        super().set_value(int(value))


class FloatField(NumberField):
    def set_value(self, value):
        super().set_value(float(value))
