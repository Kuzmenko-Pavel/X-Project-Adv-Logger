from pymongo import ASCENDING


async def check_collection(app):
    conf = app['config']['mongo']
    block = await app.block.options()
    offer = await app.offer.options()
    if not block.get('capped', False):
        print(await app.db.drop_collection(conf['collection']['block']))
        app.block = await app.db.create_collection(conf['collection']['block'],
                                                   size=700 * 1000000,
                                                   capped=True,
                                                   max=1000000)

    if not offer.get('capped', False):
        print(await app.db.drop_collection(conf['collection']['offer']))
        app.offer = await app.db.create_collection(conf['collection']['offer'],
                                                   size=700 * 1000000,
                                                   capped=True,
                                                   max=1000000)
    await app.offer.create_index('token', background=True)
    await app.offer.create_index([('ip', ASCENDING), ('cookie', ASCENDING)], background=True)


def on_startup(app):
    app.on_startup.append(check_collection)
