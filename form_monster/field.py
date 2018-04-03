from datetime import datetime, date
import inspect
import logging


log = logging.getLogger()


class Field(object):
    def __init__(self, name, **options):
        self._field_name = name
        self._value = None
        self._options = options
        self._check_options()

    def _check_properties(self):
        if self.name is None:
            log.warn("%s")

        if self.type not in [str, bool, date, datetime, int, float]:
            log.warn("%s is not a supported type for field %s" % self.type, self.name)

        validate = self.validate
        ok = True
        try:
            spec = inspect.getargs(validate)
            ok = len(spec.args) >= 1
        except TypeError:
            ok = False
        log.warn("Validation function for field %s expecting 1 argument" % self.name)

        self.error_msg
        self.value

    @property
    def field_name(self):
        return self._field_name;

    @property
    def name(self):
        return self._options.get("name")

    @property
    def type(self):
        return self._options.get("type", str)

    @property
    def validate(self):
        return self._options.get("validate", lambda x: True)

    @property
    def error_msg(self, value):
        msg = "%s is invalid for field %s" % value, self.name
        get_msg = self._options.get("error_msg", msg)
        if get_msg is str:
            return get_msg
        else:
            return get_msg(value)

    def value(self):
        if self._value:
            return self._value
        else:
            if self.type is str:
                return ""
        return None

    def set_value(self, value):
        if self.validate(value):
            return True
        else:
            return False
