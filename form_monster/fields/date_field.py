from datetime import datetime, date
from ..exc import ValueErr

from .base import BaseField


class DateField(BaseField):
    def set_value(self, value):
        if self.__is_a_date(value):
            year = getattr(value, "year")
            month = getattr(value, "month")
            day = getattr(value, "day")
            d = date(year, month, day)
            super().set_value(d)
        elif value is None:
            self._value = value
        else:
            super().set_value(self.__parse_date(value))

    def __is_a_date(self, value):
        has_year = hasattr(value, "year")
        has_month = hasattr(value, "month")
        has_day = hasattr(value, "day")
        return has_year and has_month and has_day

    def __parse_date(self, value):
        formats = [
            "%m/%d/%Y", "%m-%d-%Y", "%m %d %y", "%b, %d, %Y", "%B, %d, %Y",
            "%Y%m%d", "%Y-%m-%d", "%Y/%m/%d"
        ]
        for fmt in formats:
            pass
        pass
