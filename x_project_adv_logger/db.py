import asyncio

from motor import motor_asyncio as ma

from x_project_adv_logger.logger import logger, exception_message


class DbWrapper():
    __slots__ = ['conf', 'client', 'db', 'block_name', 'offer_name']

    def __init__(self, conf):
        self.conf = conf
        self.client = ma.AsyncIOMotorClient(conf['uri'])
        self.db = self.client[conf['db']]
        self.block_name = conf['collection']['block']
        self.offer_name = conf['collection']['offer']

    @property
    def block(self):
        return self.db[self.block_name]

    @property
    def offer(self):
        return self.db[self.offer_name]

    async def create_collection(self, collection_name):
        avg_obj_size = 500
        max_obj = 50000000
        try:
            await self.db.drop_collection(collection_name)
            await self.db.create_collection(collection_name, size=max_obj * avg_obj_size, capped=True, max=max_obj)
            if collection_name == self.conf['collection']['offer']:
                self.db[collection_name].create_index('token', background=True)
        except Exception as ex:
            logger.warning(exception_message(exc=str(ex)))
            return collection_name, False
        finally:
            return collection_name, True

    async def get_options(self, collection_name):
        options = await self.db[collection_name].options()
        return collection_name, options

    async def check_collection(self):
        tasks = []
        tasks_options = []
        block_collection_name = self.block_name
        offer_collection_name = self.offer_name
        tasks_options.append(self.get_options(block_collection_name))
        tasks_options.append(self.get_options(offer_collection_name))

        result_options = await asyncio.gather(*tasks_options)
        for collection_name, options in result_options:
            if not options.get('capped', False):
                tasks.append(self.create_collection(collection_name))
        await asyncio.gather(*tasks)


async def init_db(app):
    conf = app['config']['mongo']
    app.db = DbWrapper(conf)
    await app.db.check_collection()
