# -*- coding: utf-8 -*-

import logging

from tweetai.__version__ import (__author__, __author_email__, __copyright__,
                               __description__, __license__, __title__,
                               __url__, __version__)
from tweetai.core import TweetAI, __doc__

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Avoids "No handler found" warning when logging is not configured
logging.getLogger(__name__).addHandler(NullHandler())
