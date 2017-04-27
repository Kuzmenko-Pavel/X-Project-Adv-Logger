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
