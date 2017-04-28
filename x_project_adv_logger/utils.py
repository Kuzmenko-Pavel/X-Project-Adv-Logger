import linecache
import sys

import trafaret as T

primitive_ip_regexp = r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'

TRAFARET_CONF = T.Dict({
    T.Key('mongo'):
        T.Dict({
            'uri': T.String(),
            'db': T.String(),
            T.Key('collection'):
                T.Dict({
                    'offer': T.String(),
                    'block': T.String(),
                })
        }),
    T.Key('host'): T.String(regex=primitive_ip_regexp),
    T.Key('port'): T.Int(),
})

TRAFARET_OFFER_DATA = T.Dict({
    T.Key('informer'): T.Any,
    T.Key('params'): T.Any,
    T.Key('items'): T.List(T.Any),
})


def exception_message():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
