from datetime import datetime, date
import inspect
import logging

log = logging.getLogger()


class Field(object):
    def __init__(self, name, form={}, options={}):
        self._name = name
        self.form = form
        self._value = None
        self._options = options
        self._check_properties()

    def _check_properties(self):
        if self.type_ not in [str, bool, date, datetime, int, float]:
            log.warn("%s is not a supported type for field %s" % self.type_,
                     self.name)

        validate = self._options.get("validate", lambda x: True)
        ok = True
        try:
            spec = inspect.getargspec(validate)
            ok = len(spec.args) >= 1
        except TypeError:
            ok = False
        if not ok:
            log.warn("\"validate\" function for field %s expecting 1 argument"
                     % self.name)

        compute = self._options.get("compute", None)
        if compute is not None:
            spec = inspect.getargspec(validate)
            for arg in spec.args:
                dep = self._options.get(arg, None)
                if dep is None:
                    log.warn("Field %s is not defined" % dep)

    @property
    def name(self):
        return self._name

    @property
    def text(self):
        return self._options.get("text", self.name)

    @property
    def type_(self):
        return self._options.get("type", str)

    @property
    def is_valid(self):
        validate = self._options.get("validate", lambda x: True)
        return validate(self.value)

    @property
    def error_msg(self, value):
        msg = "%s is invalid for field %s" % value, self.name
        get_msg = self._options.get("error_msg", msg)
        if get_msg is str:
            return get_msg
        else:
            return get_msg(value)

    @property
    def _compute(self):
        return self._options.get("compute", None)

    @property
    def _validate(self):
        return self._options.get("validate", None)

    @property
    def value(self):
        if self._compute is not None:
            spec = inspect.getargspec(self._compute)
            args = []
            for field_name in spec.args:
                dep = self.form.get(field_name)
                args.append(dep.value)
            return self._compute(*args)
        if self._value:
            return self._value
        return None

    @value.setter
    def value(self, value):
        """
        for date convert a year/month/date to 20130324 ex. 19930324 is 1993/03/24
        """
        if self.type_ is date:
            self._value = datetime.strptime(value, "%Y%m%d").date()
        elif self.type_ is datetime:
            self._value = datetime.strptime(value, "%Y%m%d")
        else:
            self._value = self.type_(value)
