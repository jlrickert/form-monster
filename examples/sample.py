import logging
from datetime import datetime, date
from form_monster import Form, Web, WxView

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

class StrField():
    def __init__(self, name):
        pass

class computedField(object):
    def __init__(self, name, field):
        pass

form = Form([
    (StrField("first_text"), { "optional": True }),
    (ComputedField("full_name", StrField), { "optional": False })
])
