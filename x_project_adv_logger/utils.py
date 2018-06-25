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
    T.Key('host'): T.Regexp(primitive_ip_regexp),
    T.Key('port'): T.Int(),
})

TRAFARET_OFFER_DATA = T.Dict({
    T.Key('informer', optional=True): T.Any,
    T.Key('params'): T.Dict({
        T.Key('cookie'): T.String(),
        T.Key('informer_id'): T.String(),
        T.Key('informer_id_int'): T.Int(),
        T.Key('active'): T.String(),
        T.Key('request'): T.String(),
        T.Key('test'): T.Bool(),
    }).ignore_extra('*'),
    T.Key('items'): T.List(T.Any),
})
