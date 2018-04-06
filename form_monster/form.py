import logging
import sys
from collections import OrderedDict

from .utils import clear_screan
from .command import SetCommand
from .field import Field

log = logging.getLogger(__name__)


class Form(object):
    def __init__(self, form_data):
        self._check_for_ordered_dict(form_data)
        self._fields = self._init_fields(form_data)

    def _check_for_ordered_dict(self, d):
        is_supported_python = sys.version_info >= (3, 6)
        is_dict = type(d) is dict
        is_ordered_dict = type(d) is OrderedDict
        is_ordered = is_ordered_dict or (is_dict and is_supported_python)
        if not is_ordered:
            log.warn(
                "Form data is not an OrderedDict and order may not be perserved"
            )

    def _init_fields(self, form_data):
        fields = OrderedDict()
        for key, value in form_data.items():
            fields[key] = Field(key, options=value)
        for field in fields.values():
            for dep in field.get_dependencies():
                dep_field = fields.get(dep, None)
                if dep_field is not None:
                    field.add_dependency(dep_field)
            ok = field.check_properties()
        return fields

    def get(self, key, default=None):
        """Alias to get_field"""
        return self._fields(key, default)

    def set(self, key, value):
        self._fields[key].value = value

    @property
    def fields(self):
        return self._fields.values()

    def is_valid(self):
        for value in self.fields:
            if not value.is_valid():
                return False
        return True
