import logging
import sys
from collections import OrderedDict

from .utils import clear_screan
from .command import SetCommand
from .field import Field

log = logging.getLogger()


class Form(object):
    def __init__(self, form_data):
        is_ordered = type(form_data) is OrderedDict or sys.version_info >= (3,6)
        if not is_ordered:
            log.warn("Form data is not an OrderedDict and order may not be perserved")
        self.fields = self._init_fields(form_data)

    def _init_fields(self, form_data):
        fields = OrderedDict()
        for key, value in form_data.items():
            fields[key] = Field(key, form=self, options=value)
        return fields

    def get_field(self, key):
        return self.fields[key]

    def get(self, key, _=None):
        """Alias to get_field"""
        return self.get_field(key)

    def set(self, key, value):
        self.fields[key].value = value

    def is_valid(self):
        for key, value in self.fields.items():
            if not value.is_valid():
                return False
        return True
