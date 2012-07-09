import logging

class LoggingDecorator(object):
    def __init__(self, f):
        self.f = f

class log_call(LoggingDecorator):
    def __call__(self, *args, **kwargs):
        f = self.f
        logging.debug("%s called", f.__name__)
        rv = f(*args, **kwargs)
        logging.debug("%s returned type %s", f.__name__, type(rv))
        return rv

class log_view(LoggingDecorator):
    def __call__(self, *args, **kwargs):
        f = self.f
        logging.debug("%s called with method %s, kwargs %s", f.__name__, args[0].method, kwargs)
        rv = f(*args, **kwargs)
        logging.debug("%s returned type %s", f.__name__, type(rv))
        return rv
