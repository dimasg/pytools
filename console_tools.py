# -*- coding: utf-8 -*-

#
# Original version from http://habrahabr.ru/blogs/python/117236/
#

import sys
import codecs
import copy
import ctypes
import logging

ansi = not sys.platform.startswith("win")


def setup_console(sys_enc='utf-8', use_colorama=True):
    """
    Set sys.defaultencoding to `sys_enc` and update stdout/stderr writers
    to corresponding encoding

    .. note:: For Win32 the OEM console encoding will be used istead
    of `sys_enc`
    """
    global ansi
    reload(sys)
    try:
        if sys.platform.startswith("win"):
            enc = "cp%d" % ctypes.windll.kernel32.GetOEMCP()
        else:
            enc = (sys.stdout.encoding if sys.stdout.isatty() else
                   sys.stderr.encoding if sys.stderr.isatty() else
                   sys.getfilesystemencoding() or sys_enc)

        sys.setdefaultencoding(sys_enc)

        if sys.stdout.isatty() and sys.stdout.encoding != enc:
            sys.stdout = codecs.getwriter(enc)(sys.stdout, 'replace')

        if sys.stderr.isatty() and sys.stderr.encoding != enc:
            sys.stderr = codecs.getwriter(enc)(sys.stderr, 'replace')

        if use_colorama and sys.platform.startswith("win"):
            try:
                from colorama import init
                init()
                ansi = True
            except:
                pass

    except:
        pass


class ColoredHandler(logging.StreamHandler):
    def emit(self, record):
        # Need to make a actual copy of the record
        # to prevent altering the message for other loggers
        myrecord = copy.copy(record)
        levelno = myrecord.levelno
        if(levelno >= 50):  # CRITICAL / FATAL
            color = '\x1b[31;1m'  # red
        elif(levelno >= 40):  # ERROR
            color = '\x1b[31m'  # red
        elif(levelno >= 30):  # WARNING
            color = '\x1b[33m'  # yellow
        elif(levelno >= 20):  # INFO
            color = '\x1b[32m'  # green
        elif(levelno >= 10):  # DEBUG
            color = '\x1b[35m'  # pink
        else:  # NOTSET and anything else
            color = '\x1b[0m'  # normal
        myrecord.msg = (u"%s%s%s" % (color, myrecord.msg, '\x1b[0m'))\
                            .encode('utf-8')  # normal
        logging.StreamHandler.emit(self, myrecord)
