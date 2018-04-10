import inspect
from ..exc import ValueErr


class BaseField():
    def __init__(self,
                 text,
                 optional=True,
                 compute=None,
                 dependencies=[],
                 validate=None):
        self._value = None
        self.text = text
        self.optional = optional
        self.compute = compute
        self.dependencies = dependencies
        self._validate = validate

    def validate(self, value):
        must_have_value = self.optional is False
        value_is_none = self._value is None
        if must_have_value and value_is_none:
            return False
        if self._validate:
            return self._validate(value)
        return True

    def is_valid(self):
        return self.validate(self.get_value())

    def get_value(self, default=object):
        if self.compute:
            return self._get_computed_value()

        is_invalid = not self.validate(self._value)
        has_alt_value = default is not object
        if is_invalid and has_alt_value:
            return default

        return self._value

    def _get_computed_value(self):
        deps = [dep.get_value(None) for dep in self.dependencies]
        return self.compute(*deps)

    def set_value(self, value):
        if not self.compute:
            self._value = value

    def __str__(self):
        if self._value is None:
            return ""
        return str(self._value)
