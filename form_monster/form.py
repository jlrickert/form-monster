import logging
import sys
from copy import deepcopy

from .utils import clear_screan

log = logging.getLogger(__name__)

class Form(object):
    def __init__(self, fields={}):
        self.__fields = {}
        self.set_fields(fields)

    def get_field(self, name):
        return self.__fields[name]

    def get_fields(self):
        return self.__fields.items()

    def get_value(self, name, default=None):
        return self.__fields[name].get_value(default)

    def set_field(self, name, field, deps=[]):
        dependencies = [self.__fields[dep] for dep in deps]
        self.__fields[name] = deepcopy(field)

    def set_fields(self, fields={}):
        link = {}
        print("v", [id(v) for v in fields.values()])
        for name, field in fields.items():
            field_ = deepcopy(field)
            field_._dependencies = field._dependencies
            link[field] = field_
            self.__fields[name] = field_

        self.__fix_dependencies(link)


    def __fix_dependencies(self, link):
        for field in self.__fields.values():
            for i in range(len(field._dependencies)):
                dep = field._dependencies[i]
                if type(dep) is str:
                    field._dependencies[i] = self.__fields[dep]
                elif dep in link:
                    field._dependencies[i] = link[dep]
                else:
                    pass

    def set_value(self, name, value):
        self.__fields[name].set_value(value)

    def is_valid(self):
        for field in self.__fields.values():
            if not field.is_valid():
                return False
        return True

    def finalize(self):
        return {(key, value.get_value()) for key, field in self.__form}
