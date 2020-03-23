from datetime import datetime

from aiohttp import web
from aiojobs.aiohttp import spawn
from pymongo import InsertOne
from pymongo.errors import BulkWriteError
from trafaret.constructor import construct

from x_project_adv_logger.headers import *
from x_project_adv_logger.logger import logger, exception_message
from x_project_adv_logger.utils import TRAFARET_OFFER_DATA


async def bulk_write(collectin, docs):
    try:
        await collectin.bulk_write(docs)
    except BulkWriteError as ex:
        logger.warning(exception_message(exc=str(ex), docs=docs))


class OfferView(web.View):
    @detect_ip()
    @cookie()
    @cors(allow_origin='*')
    @xml_http_request()
    async def post(self):
        docs = []
        data = None
        try:
            validator = construct(TRAFARET_OFFER_DATA)
            data = await self.request.json()
            validator(data)
        except Exception as ex:
            logger.warning(exception_message(exc=str(ex), data=data, request=str(self.request.message)))
        else:
            try:
                test = data['p']['t']
                if not test:
                    ip = self.request.ip
                    cookie = data['p']['c']
                    request = data['p'].get('r', 'initial')
                    active = data['p'].get('a', 'initial')
                    dt = datetime.now()
                    id_block = data['b']['id']
                    id_site = data['b']['sid']
                    id_account_right = data['b']['aid']
                    vw = data['b'].get('vw', '')
                    vh = data['b'].get('vh', '')
                    w = data['b'].get('w', '')
                    h = data['b'].get('h', '')
                    loc = data['b'].get('loc', '')
                    ref = data['b'].get('ref', '')
                    if len(data['i']) <= 0:
                        raise Exception('Offer count 0')

                    for i in data['i']:
                        id_offer = i['id']
                        id_campaign = i['cid']
                        id_account_left = i['aid']
                        impressions_block = i['ib']
                        social = i['s']
                        impressions_cost_right = i['icr']
                        impressions_cost_left = i['icl']
                        token = i['t']
                        doc = {
                            'ip': ip,
                            'cookie': cookie,
                            'request': request,
                            'test': test,
                            'active': active,
                            'dt': dt,
                            'vw': vw,
                            'vh': vh,
                            'w': w,
                            'h': h,
                            'loc': loc,
                            'ref': ref,
                            'id_block': id_block,
                            'id_site': id_site,
                            'id_account_right': id_account_right,
                            'id_offer': id_offer,
                            'id_campaign': id_campaign,
                            'id_account_left': id_account_left,
                            'impressions_block': impressions_block,
                            'social': social,
                            'token': token,
                            'impressions_cost_right': impressions_cost_right,
                            'impressions_cost_left': impressions_cost_left
                        }
                        docs.append(InsertOne(doc))
                    if len(docs) > 0:
                        await spawn(self.request, bulk_write(self.request.app.db.offer, docs))
            except Exception as ex:
                logger.warning(exception_message(exc=str(ex), data=data, request=str(self.request.message)))
        return web.json_response({'status': 'ok'})