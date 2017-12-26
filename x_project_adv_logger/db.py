from motor import motor_asyncio as ma
from pymongo import ASCENDING

from x_project_adv_logger.logger import logger, exception_message


async def init_db(app):
    conf = app['config']['mongo']
    app.client = ma.AsyncIOMotorClient(conf['uri'])
    app.db = app.client[conf['db']]
    app.block = app.db[conf['collection']['block']]
    app.offer = app.db[conf['collection']['offer']]
    block = await app.block.options()
    offer = await app.offer.options()
    if not block.get('capped', False):
        try:
            await app.db.drop_collection(conf['collection']['block'])
            app.block = await app.db.create_collection(conf['collection']['block'],
                                                       size=700 * 1000000,
                                                       capped=True,
                                                       max=1000000)
        except Exception as ex:
            logger.debug(exception_message(exc=str(ex)))

    if not offer.get('capped', False):
        try:
            await app.db.drop_collection(conf['collection']['offer'])
            app.offer = await app.db.create_collection(conf['collection']['offer'],
                                                       size=700 * 1000000,
                                                       capped=True,
                                                       max=1000000)
        except Exception as ex:
            logger.debug(exception_message(exc=str(ex)))

    await app.offer.create_index('token', background=True)
    await app.offer.create_index([('ip', ASCENDING), ('cookie', ASCENDING)], background=True)
