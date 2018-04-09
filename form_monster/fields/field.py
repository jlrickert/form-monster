from datetime import datetime, date
import inspect
import logging

log = logging.getLogger(__name__)


class Field(object):
    def __init__(self, name, dependencies=[], options={}):
        self._name = name
        self._dep_fields = {field.name: field for field in dependencies}
        self._value = None
        self._options = options

    def check_properties(self):
        """Ensures the the field is logically correct"""
        is_ok = True
        is_ok = is_ok and self._check_type()
        is_ok = is_ok and self._check_validate_func()
        is_ok = is_ok and self._check_compute_func()
        return is_ok

    def _check_type(self):
        if self.type_ not in [str, bool, date, int, float]:
            log.warn("%s is not a supported type for field %s" % self.type_,
                     self.name)
            return False
        return True

    def _check_validate_func(self):
        ok = True
        try:
            validate = self._get_validate_fn()
            spec = inspect.getargspec(validate)
            ok = len(spec.args) == 1
        except TypeError:
            ok = False

        if not ok:
            log.warn(
                "\"validate\" function for field %s expecting only 1 argument"
                % self.name)
        return ok

    def _check_compute_func(self):
        compute = self._get_compute_fn()
        if compute is None:
            return True

        ok = True
        for arg in self.get_dependencies():
            dep = self._dep_fields.get(arg, None)
            if dep is None:
                ok = False
                log.warn("Field %s is not defined. Needed by field %s" %
                         (dep, self.name))
        return ok

    def add_dependency(self, field):
        self._dep_fields[field.name] = field

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
        validate = self._get_validate_fn()
        return validate(self.value)

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

    def get_dependencies(self):
        compute = self._get_compute_fn()
        if compute is None:
            return []
        spec = inspect.getargspec(compute)
        return spec.args

    @property
    def value(self):
        compute = self._get_compute_fn()
        if compute is not None:
            args = []
            for field_name in self.get_dependencies():
                dep = self._dep_fields.get(field_name)
                args.append(dep.value)
            return compute(*args)
        if self._value:
            if self.type_ == date:
                return self._calc_date(self._value)
            return self._value
        return None

    def _calc_date(self, date_str):
        for fmt in ["%m/%d/%Y", "%Y%m%d"]:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                pass
        raise ValueError("%s is an invalid formated date" % date_str)

    @value.setter
    def value(self, value):
        """
        For date convert a month/day/year. ex. 02/30/1992
        """
        if self.type_ is date:
            self._value = value
        else:
            self._value = self.type_(value)

    def validate(self, value):
        fn = self._get_validate_fn()
        if self.type_ is date:
            pass
        return fn(value)

    def _get_validate_fn(self):
        return self._options.get("validate", lambda x: True)

    def compute(self, *args):
        fn = self._get_compute_fn()
        return fn(*args)

    def _get_compute_fn(self):
        return self._options.get("compute", None)

    @property
    def _optional(self):
        is_optional = self._options.get("optional", None)
        is_nullable = self._options.get("nullable", None)
        return (is_optional is None and is_nullable is None
                ) or is_optional is True or is_nullable is True
