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
    T.Key('b'): T.Dict({
        T.Key('id'): T.String(),
        T.Key('sid'): T.String(),
        T.Key('aid'): T.String(),
    }).ignore_extra('*'),
    T.Key('p'): T.Dict({
        T.Key('c'): T.String(allow_blank=True),
        T.Key('r'): T.String(),
        T.Key('a'): T.String(),
        T.Key('t'): T.Bool(),
    }).ignore_extra('*'),
    T.Key('i'): T.List(
        T.Dict({
            T.Key('id'): T.String(),
            T.Key('cid'): T.String(),
            T.Key('aid'): T.String(),
            T.Key('ib'): T.Float(),
            T.Key('s'): T.Bool(),
            T.Key('icr'): T.Float(),
            T.Key('icl'): T.Float(),
            T.Key('t'): T.String(),
        }).ignore_extra('*')
    )
})
