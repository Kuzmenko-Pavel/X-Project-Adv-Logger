from datetime import datetime

from aiohttp import web
from pymongo import InsertOne
from trafaret.constructor import construct

from ..utils import TRAFARET_OFFER_DATA, exception_message


class OfferView(web.View):
    async def post(self):
        docs = []
        if self.request.is_xml_http:
            try:
                validator = construct(TRAFARET_OFFER_DATA)
                data = await self.request.json()
                validator(data)
            except Exception as e:
                self.request.app['log'].debug(exception_message())
            else:
                inf = data['params']['informer_id_int']
                inf_int = data['params']['informer_id']
                ip = data['params']['ip']
                cookie = data['params']['cookie']
                country = data['params']['country']
                region = data['params']['region']
                request = data['params']['request']
                test = data['params']['test']
                dt = datetime.now()
                for i in data['items']:
                    doc = {}
                    doc['dt'] = dt
                    doc['id'] = i['guid']
                    doc['id_int'] = i['id']
                    doc['title'] = i['title']
                    doc['inf'] = inf
                    doc['inf_int'] = inf_int
                    doc['ip'] = ip
                    doc['cookie'] = cookie
                    doc['social'] = i['campaign_social']
                    doc['token'] = i['token']
                    doc['type'] = 'teaser'
                    doc['isOnClick'] = True
                    doc['campaignId'] = i['campaign_guid']
                    doc['account_id'] = i['campaign_account']
                    doc['campaignId_int'] = i['campaign_id']
                    doc['campaignTitle'] = i['campaign_title']
                    doc['project'] = i['campaign_project']
                    doc['country'] = country
                    doc['region'] = region
                    doc['retargeting'] = i['retargeting']
                    doc['keywords'] = {'search': '', 'context': ''}
                    doc['branch'] = i['branch']
                    doc['conformity'] = 'place'
                    doc['matching'] = ''
                    doc['test'] = test
                    doc['request'] = request
                    docs.append(InsertOne(doc))
            if len(docs) > 0:
                await self.request.app.offer.bulk_write(docs)
        resp_data = {'status': self.request.is_xml_http}
        return web.json_response(resp_data)
