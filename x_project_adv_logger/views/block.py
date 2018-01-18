from datetime import datetime

from aiohttp import web

from x_project_adv_logger.headers import *


class BlockView(web.View):
    @cors(allow_origin='*')
    async def get(self):
        doc = {}
        headers = self.request.headers
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
        else:
            doc['dt'] = dt
            doc['guid'] = guid
            doc['garanted'] = garanted
            await self.request.app.db.block.insert(doc)
        return web.Response(body=body, content_type='application/x-javascript', charset='utf-8')

    @xml_http_request()
    @cors(allow_origin='*')
    async def post(self):
        doc = {}
        headers = self.request.headers
        post = await self.request.post()
        guid = post.get('guid', self.request.query.get('guid', ''))
        request = post.get('request', self.request.query.get('request', 'initial'))
        rand = post.get('rand', self.request.query.get('rand', ''))
        garanted = True if request == 'complite' else False
        dt = datetime.now()
        if headers.get('Referer', '') != '':
            doc['dt'] = dt
            doc['guid'] = guid
            doc['garanted'] = garanted
            await self.request.app.block.insert_one(doc)
        resp_data = {'status': self.request.is_xml_http}
        return web.json_response(resp_data)
