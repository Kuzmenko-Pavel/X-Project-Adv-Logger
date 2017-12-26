from pymongo import ASCENDING

from x_project_adv_logger.utils import exception_message


async def check_collection(app):
    conf = app['config']['mongo']
    block = await app.block.options()
    offer = await app.offer.options()
    print(block)
    print(offer)
    if not block.get('capped', False):
        try:
            await app.db.drop_collection(conf['collection']['block'])
            app.block = await app.db.create_collection(conf['collection']['block'],
                                                       size=700 * 1000000,
                                                       capped=True,
                                                       max=1000000)
        except Exception as e:
            app['log'].debug(exception_message())

    if not offer.get('capped', False):
        try:
            await app.db.drop_collection(conf['collection']['offer'])
            app.offer = await app.db.create_collection(conf['collection']['offer'],
                                                       size=700 * 1000000,
                                                       capped=True,
                                                       max=1000000)
        except Exception as e:
            app['log'].debug(exception_message())

    await app.offer.create_index('token', background=True)
    await app.offer.create_index([('ip', ASCENDING), ('cookie', ASCENDING)], background=True)


def on_startup(app):
    app.on_startup.append(check_collection)
