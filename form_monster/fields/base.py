import inspect
from ..exc import ValueErr


class BaseField():
    def __init__(self,
                 text=None,
                 optional=False,
                 compute=None,
                 dependencies=[],
                 validate=None,
                 choices=None,
                 form=None):
        """`optional` option is ignored if `validate` is not none"""
        self.__value = None
        self.text = text
        self.optional = optional
        self.__compute = compute
        self._dependencies = dependencies
        self.choices = choices
        self.__validate = validate
        self.__form = form

    def validate(self, value):
        if self.__validate:
            return self.__validate(value)
        return True

    def _hook_form(self, form, dependencies=[]):
        self.__form = form
        self._dependencies = dependencies

    def is_valid(self):
        value = self.get_value()
        if self.choices is not None and value in self.choices:
            return True

        if value is None:
            return self.optional
        return self.validate(value)

    def get_value(self, default=object):
        if self.__compute:
            return self.__get_computed_value()

        is_invalid = not self.validate(self.__value)
        has_alt_value = default is not object
        if is_invalid and has_alt_value:
            return default

        return self.__value

    def __get_computed_value(self):
        deps = []
        for dep in self._dependencies:
            value = dep.get_value(None)
            if not dep.optional and value is None:
                return
            deps.append(value)
        return self.__compute(*deps)

    def __get_dep(self, dep):
        if issubclass(type(dep), BaseField):
            return dep
        else:
            return self.form.get_field(dep)

    def set_value(self, value):
        if not self.__compute:
            self.__value = value

    def __str__(self):
        if self.__value is None:
            return ""
        return str(self.__value)
