from datetime import datetime

from aiohttp import web
from pymongo import InsertOne
from trafaret.constructor import construct

from x_project_adv_logger.headers import *
from x_project_adv_logger.utils import TRAFARET_OFFER_DATA, exception_message


class OfferView(web.View):
    @xml_http_request()
    async def post(self):
        docs = []
        try:
            validator = construct(TRAFARET_OFFER_DATA)
            data = await self.request.json()
            validator(data)
        except Exception as e:
            self.request.app['log'].warning(exception_message(exc=str(e), request=str(self.request._message)))
        else:
            try:
                inf = data['params']['informer_id']
                inf_int = data['params']['informer_id_int']
                ip = data['params']['ip']
                cookie = data['params']['cookie']
                request = data['params']['request']
                test = data['params']['test']
                dt = datetime.now()
                for i in data['items']:
                    doc = {}
                    doc['dt'] = dt
                    doc['id'] = i['guid']
                    doc['id_int'] = i['id']
                    doc['inf'] = inf
                    doc['inf_int'] = inf_int
                    doc['ip'] = ip
                    doc['cookie'] = cookie
                    doc['social'] = i['campaign_social']
                    doc['token'] = i['token']
                    doc['campaignId'] = i['campaign_guid']
                    doc['campaignId_int'] = i['campaign_id']
                    doc['retargeting'] = i['retargeting']
                    doc['branch'] = i['branch']
                    doc['conformity'] = 'place'
                    doc['test'] = test
                    doc['request'] = request
                    docs.append(InsertOne(doc))
            except Exception as e:
                self.request.app['log'].warning(exception_message(exc=str(e),
                                                                  data=data,
                                                                  request=str(self.request._message)))
        if len(docs) > 0:
            await self.request.app.offer.bulk_write(docs)
        else:
            self.request.app['log'].warning('EMPTY %s' % str(self.request._message))
        resp_data = {'status': self.request.is_xml_http}
        return web.json_response(resp_data)
