from __future__ import print_function, unicode_literals
import sys
import logbook
from logbook.more import ExceptionHandler

class ApplicationWarning(Exception):
    pass

LOGGER = logbook.Logger('Nikola')
STRICT_HANDLER = ExceptionHandler(ApplicationWarning, level='WARNING')

if sys.version_info[0] == 3:
    # Python 3
    bytes_str = bytes
    unicode_str = str
    unichr = chr
    from imp import reload as _reload
else:
    bytes_str = str
    unicode_str = unicode  # NOQA
    _reload = reload  # NOQA
    unichr = unichr

