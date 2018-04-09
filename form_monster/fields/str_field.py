from .base import BaseField


class StrField(BaseField):
    _IDENTITY = ""

    def set_value(self, value):
        super().set_value(str(value))
