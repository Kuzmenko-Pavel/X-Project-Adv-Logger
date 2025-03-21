from datetime import datetime

from aiohttp import web
from aiojobs.aiohttp import spawn
from pymongo import InsertOne
from pymongo.errors import BulkWriteError

from x_project_adv_logger.headers import *
from x_project_adv_logger.logger import logger, exception_message


async def bulk_write(collectin, docs):
    try:
        await collectin.bulk_write(docs)
    except BulkWriteError as ex:
        logger.warning(exception_message(exc=str(ex), docs=docs))


class BlockView(web.View):
    @detect_ip()
    @cookie()
    @cors(allow_origin='*')
    async def get(self):
        doc = {}
        headers = self.request.headers
        ip = self.request.ip
        guid = self.request.query.get('guid', '')
        request = self.request.query.get('request', 'initial')
        rand = self.request.query.get('rand', '')
        garanted = True if request == 'complite' else False
        dt = datetime.now()
        body = "//<![CDATA[\neval(function(p,a,c,k,e,d){e=function(c){return c};if(!''.replace(/^/,String))" \
               "{while(c--){d[c]=k[c]||c}k=[function(e){return d[e]}];e=function(){return'\\\\w+'};c=1};while(c--){if(k[c])" \
               "{p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c])}}return p}('3 0=4.5(6);2(0){2(0.1){0.1.7(0)}};" \
               "',8,8,'el|parentNode|if|var|document|getElementById|\"yt" + str(
            rand) + "\"|removeChild'.split('|'),0,{}))\n//]]>"
        if len(headers.get('Referer', '')) < 10:
            body = 'yta = {}'

        doc['dt'] = dt
        doc['guid'] = guid
        doc['ip'] = ip
        doc['garanted'] = garanted
        await spawn(self.request, bulk_write(self.request.app.db.block, [InsertOne(doc)]))
        return web.Response(body=body, content_type='application/x-javascript', charset='utf-8')

    @detect_ip()
    @cors(allow_origin='*')
    @xml_http_request()
    async def post(self):
        doc = {}
        ip = self.request.ip
        post = await self.request.post()
        guid = post.get('guid', self.request.query.get('guid', ''))
        request = post.get('request', self.request.query.get('request', 'initial'))
        garanted = True if request == 'complite' else False
        dt = datetime.now()
        doc['dt'] = dt
        doc['guid'] = guid
        doc['ip'] = ip
        doc['garanted'] = garanted
        await spawn(self.request, bulk_write(self.request.app.db.block, [InsertOne(doc)]))
        resp_data = {'status': self.request.is_xml_http}
        return web.json_response(resp_data)

    @cors(allow_origin='*')
    async def options(self):
        return web.Response()
