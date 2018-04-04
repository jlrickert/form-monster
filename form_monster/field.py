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
        if self._options.get("text", None) is None:
            log.warn('"text" is not set for field %s' % self.name)
        if self.type_ not in [str, bool, date, datetime, int, float]:
            log.warn("%s is not a supported type for field %s" % self.type_,
                     self.name)

        ok = True
        try:
            spec = inspect.getargspec(self._validate)
            ok = len(spec.args) >= 1
        except TypeError:
            ok = False
        if not ok:
            log.warn("\"validate\" function for field %s expecting 1 argument"
                     % self.name)

        if self._compute is not None:
            spec = inspect.getargspec(self._compute)
            for arg in spec.args:
                dep = self._options.get(arg, None)
                if dep is None:
                    log.warn("Field %s is not defined. Needed by field %s" % (dep, self.name))

    @property
    def name(self):
        return self._name

    @property
    def text(self):
        return self._options.get("text", self.name)

    @property
    def type_(self):
        return self._options.get("type", str)

    def is_valid(self):
        if self._optional and self.value is None:
            return True
        elif type(self.value) is not self.type_:
            return False
        return self._validate(self.value)

    def error_msg(self):
        msg = ""
        if self.value is not None:
            msg = "%s is invalid for field %s" % (self.value, self.name)
            get_msg = self._options.get("error_msg", msg)
        else:
            get_msg = 'Field "%s" is missing a value' % self.name

        if type(get_msg) is str:
            return get_msg
        else:
            return get_msg(self.value)

    @property
    def _compute(self):
        return self._options.get("compute", None)

    @property
    def _validate(self):
        return self._options.get("validate", lambda x: True)

    @property
    def _optional(self):
        is_optional = self._options.get("optional", None)
        is_nullable = self._options.get("nullable", None)
        return (is_optional is None and is_nullable is None
                ) or is_optional is True or is_nullable is True

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
        For date convert a year/month/date to 20130324 ex. 19930324 is 1993/03/24
        """
        if self.type_ is date:
            self._value = datetime.strptime(value, "%Y%m%d").date()
        elif self.type_ is datetime:
            self._value = datetime.strptime(value, "%Y%m%d")
        else:
            self._value = self.type_(value)
