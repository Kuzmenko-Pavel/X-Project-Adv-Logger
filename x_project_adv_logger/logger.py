import linecache
import logging
import os
import pprint
import sys
import traceback

dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('x_project_adv_logger')
f = logging.Formatter('[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(f)
logger.addHandler(consoleHandler)


def exception_message(msg=None, *args, **kwargs):
    params = {'args': args, 'kwargs': kwargs}
    exc_type, exc_obj, tb = sys.exc_info()
    if msg:
        return '\nMSG:{}\nPARAMS:\n{}\n\n'.format(msg, pprint.pformat(params))
    elif exc_type and exc_obj and tb:
        f = tb.tb_frame
        trace = ''.join(traceback.format_tb(tb))
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        return '\nEXCEPTION IN {} LINE {} \n"{}": {} {} \nPARAMS:\n{}\n\n'.format(
            filename, lineno, line.strip(), exc_obj, trace, pprint.pformat(params))
    else:
        return '\nPARAMS:\n{}\n\n'.format(pprint.pformat(params))
