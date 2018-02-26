import asyncio
from datetime import datetime

from motor import motor_asyncio as ma
from pymongo import ASCENDING

from x_project_adv_logger.logger import logger, exception_message


class DbWrapper():
    __slots__ = ['conf', 'client', 'dbs_name', 'dbs']

    def __init__(self, conf):
        self.conf = conf
        self.client = ma.AsyncIOMotorClient(conf['uri'])
        self.dbs_name = ['rg_%s' % x for x in range(0, 24)]
        self.dbs = {db_name: self.client[db_name] for db_name in self.dbs_name}

    @property
    def db(self):
        return self.get_db()

    def get_db(self, db_name=None):
        if db_name is None:
            now = datetime.now()
            db_name = 'rg_%s' % now.hour
        return self.dbs[db_name]

    @property
    def offer(self):
        return self.get_offer()

    def get_offer(self, db_name=None):
        db = self.get_db(db_name)
        return db[self.conf['collection']['offer']]

    @property
    def block(self):
        return self.get_block()

    def get_block(self, db_name=None):
        db = self.get_db(db_name)
        return db[self.conf['collection']['block']]

    async def create_collection(self, db_name, collection_name):
        avg_obj_size = 416
        max_obj = 2147483647
        try:
            db = self.get_db(db_name)
            await db.drop_collection(collection_name)
            await db.create_collection(collection_name, size=max_obj * avg_obj_size, capped=True, max=max_obj)
            if collection_name == self.conf['collection']['offer']:
                db[collection_name].create_index('token', background=True)
                db[collection_name].create_index([('ip', ASCENDING), ('cookie', ASCENDING)], background=True)
        except Exception as ex:
            logger.warning(exception_message(exc=str(ex)))
            return db_name, collection_name, False
        finally:
            return db_name, collection_name, True

    async def get_options(self, db_name, collection_name):
        db = self.get_db(db_name)
        options = await db[collection_name].options()
        return db_name, collection_name, options

    async def check_collection(self):
        tasks = []
        tasks_options = []
        block_collection_name = self.conf['collection']['block']
        offer_collection_name = self.conf['collection']['offer']
        for db_name in self.dbs_name:
            tasks_options.append(self.get_options(db_name, block_collection_name))
            tasks_options.append(self.get_options(db_name, offer_collection_name))

        result_options = await asyncio.gather(*tasks_options)
        for db_name, collection_name, options in result_options:
            if not options.get('capped', False):
                tasks.append(self.create_collection(db_name, collection_name))
        await asyncio.gather(*tasks)


async def init_db(app):
    conf = app['config']['mongo']
    app.db = DbWrapper(conf)
    await app.db.check_collection()
