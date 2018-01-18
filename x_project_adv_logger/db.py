from motor import motor_asyncio as ma


class QueryWrapper():
    __slots__ = ['log_type']

    def __init__(self, log_type):
        self.log_type = log_type

    async def insert(self, doc):
        if self.log_type == 'offer':
            await self.request.app.offer.bulk_write(doc)
        elif self.log_type == 'block':
            await self.request.app.block.insert_one(doc)


def init_db(app):
    conf = app['config']['mongo']
    app.client = ma.AsyncIOMotorClient(conf['uri'])
    app.dbs_name = ['rg_%s' % x for x in range(0, 24)]
    app.dbs_name.append('getmyad')
    app.dbs = [app.client[db_name] for db_name in app.dbs_name]
    app.block = QueryWrapper('block')
    app.offer = QueryWrapper('offer')


async def check_collection(app):
    conf = app['config']['mongo']
    # block = await app.block.options()
    # offer = await app.offer.options()
    # print(block)
    # print(offer)
    # if not block.get('capped', False):
    #     try:
    #         await app.db.drop_collection(conf['collection']['block'])
    #         app.block = await app.db.create_collection(conf['collection']['block'],
    #                                                    size=700 * 1000000,
    #                                                    capped=True,
    #                                                    max=1000000)
    #     except Exception as e:
    #         app['log'].debug(exception_message())
    #
    # if not offer.get('capped', False):
    #     try:
    #         await app.db.drop_collection(conf['collection']['offer'])
    #         app.offer = await app.db.create_collection(conf['collection']['offer'],
    #                                                    size=700 * 1000000,
    #                                                    capped=True,
    #                                                    max=1000000)
    #     except Exception as e:
    #         app['log'].debug(exception_message())
    #
    # await app.offer.create_index('token', background=True)
    # await app.offer.create_index([('ip', ASCENDING), ('cookie', ASCENDING)], background=True)
