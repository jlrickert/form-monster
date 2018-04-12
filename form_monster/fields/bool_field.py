
from .base import BaseField


class BoolField(BaseField):
    def set_values(self, value):
        super().set_value(bool(value))
