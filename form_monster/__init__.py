"""
Form Monster {version}

"""

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = '0.0.1a2'
__doc__ = __doc__.format(version=__version__)

from .form import Form
from .view import Console
from .field import Field
