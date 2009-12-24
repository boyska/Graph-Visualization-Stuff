'''
Provides logging/debugging feature

How to use
==========
    You just need to import this module, and you can use our easy methods::

        import debugger
        debugger.debug('Some text')

    Levels
    ------
        Not every debug text is equally important.  That's why we have logging
        levels: info, debug, warning, error, critical The functions follows the
        same name of the levels, and all behave the same way.  Thanks to
        levels, you can put lot of debug info without having your console full
        of unimportant messages.
'''

import time
import logging
from collections import deque

import inspect
import os.path

def _build_caller():
    #Get class.method_name
    caller_obj = inspect.stack()[2]
    try:
        parent_class = '%s.' % caller_obj[0].f_locals['self'].__class__.__name__
    except:
        parent_class = ''
    class_method = '%s%s' % (parent_class, caller_obj[3])
    #filename = caller_obj[0].f_code.co_filename
    #caller = '%s' % (os.path.basename(filename).split('.py')[0])
    return class_method

def dbg(text, caller=None, level=1):
    '''
    DEPRECATED! debug the code through our mighty debugger: compatibility function
    '''
    if not caller:
        caller = _build_caller()

    #old_dbg(text, module, level)
    _logger.log(level*10, text, extra={'caller':caller})

def log(text, caller=None):
    '''
    log something through our mighty debugger
    '''
    if not caller:
        caller = _build_caller()
    _logger.log(level, text, extra={'caller':caller})


def debug(text, caller=None):
    '''
    log something through our mighty debugger
    '''
    if not caller:
        caller = _build_caller()
    _logger.debug(text, extra={'caller':caller})


def info(text, caller=None):
    '''
    log something through our mighty debugger
    '''
    if not caller:
        caller = _build_caller()
    _logger.info(text, extra={'caller':caller})


def warning(text, caller=None):
    '''
    log something through our mighty debugger
    '''
    if not caller:
        caller = _build_caller()
    _logger.warning(text, extra={'caller':caller})


def error(text, caller=None):
    '''
    log something through our mighty debugger
    '''
    if not caller:
        caller = _build_caller()
    _logger.error(text, extra={'caller':caller})


def critical(text, caller):
    '''
    log something through our mighty debugger
    '''
    if not caller:
        caller = _build_caller()
    _logger.critical(text, extra={'caller':caller})


class QueueHandler(logging.Handler):
    '''
    An Handler that just keeps the last messages in memory, using a queue.
    This is useful when you want to know (i.e. in case of errors) the last
    debug messages.
    '''
    def __init__(self, maxlen=50):
        logging.Handler.__init__(self)
        self.queue = deque(maxlen=maxlen)

    def emit(self, record):
        self.queue.append(record)

    def get_all(self):
        l = len(self.queue)
        for i in range(l):
            record = self.queue.pop()
            self.queue.appendleft(record)
            yield record

_logger = logging.getLogger('emesene')
_console_handler = logging.StreamHandler()
_formatter = logging.Formatter('[%(caller)s] %(message)s', '%H:%M:%S')
_console_handler.setFormatter(_formatter)
_console_handler.setLevel(logging.DEBUG)
_logger.addHandler(_console_handler)

queue_handler = QueueHandler()
queue_handler.setLevel(logging.DEBUG)
_logger.addHandler(queue_handler)

_logger.setLevel(logging.DEBUG)


