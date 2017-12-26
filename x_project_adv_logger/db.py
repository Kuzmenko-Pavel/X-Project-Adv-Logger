from motor import motor_asyncio as ma

def init_db(app):
    conf = app['config']['mongo']
    app.client = ma.AsyncIOMotorClient(conf['uri'])
    app.dbs_name = ['rg_%s' % x for x in range(0, 24)]
    app.dbs_name.append('getmyad')
    app.dbs = [app.client[db_name] for db_name in app.dbs_name]
    app.block = app.db[conf['collection']['block']]
    app.offer = app.db[conf['collection']['offer']]
