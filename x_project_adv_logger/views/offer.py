from datetime import datetime

from aiohttp import web
from pymongo import InsertOne
from trafaret.constructor import construct

from x_project_adv_logger.headers import *
from x_project_adv_logger.logger import logger, exception_message
from x_project_adv_logger.utils import TRAFARET_OFFER_DATA


class OfferView(web.View):
    @xml_http_request()
    async def post(self):
        docs = []
        try:
            validator = construct(TRAFARET_OFFER_DATA)
            data = await self.request.json()
            validator(data)
        except Exception as ex:
            logger.warning(exception_message(exc=str(ex), data=data, request=str(self.request.message)))
        else:
            try:
                inf = data['params']['informer_id']
                inf_int = int(data['params']['informer_id_int'])
                ip = data['params']['ip']
                cookie = data['params']['cookie']
                request = data['params']['request']
                test = data['params']['test']
                dt = datetime.now()
                for i in data['items']:
                    doc = {}
                    doc['dt'] = dt
                    doc['id'] = i['guid']
                    doc['id_int'] = int(i['id'])
                    doc['inf'] = inf
                    doc['inf_int'] = inf_int
                    doc['ip'] = ip
                    doc['cookie'] = cookie
                    doc['social'] = i['campaign_social']
                    doc['token'] = i['token']
                    doc['campaignId'] = i['campaign_guid']
                    doc['campaignId_int'] = int(i['campaign_id'])
                    doc['retargeting'] = i['retargeting']
                    doc['branch'] = i['branch']
                    doc['conformity'] = 'place'
                    doc['test'] = test
                    doc['request'] = request
                    docs.append(InsertOne(doc))
            except Exception as ex:
                logger.warning(exception_message(exc=str(ex), data=data, request=str(self.request.message)))

        if len(docs) > 0:
            await self.request.app.db.offer.bulk_write(docs)
        else:
            logger.warning(exception_message(data=data, request=str(self.request.message)))
        return web.json_response({'status': 'ok'})
