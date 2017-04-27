from aiohttp import web


class BlockView(web.View):
    async def get(self):
        headers = self.request.headers
        guid = self.request.query.get('guid')
        request = self.request.query.get('request')
        rand = self.request.query.get('rand', '')
        body = "//<![CDATA[\neval(function(p,a,c,k,e,d){e=function(c){return c};if(!''.replace(/^/,String))" \
               "{while(c--){d[c]=k[c]||c}k=[function(e){return d[e]}];e=function(){return'\\\\w+'};c=1};while(c--){if(k[c])" \
               "{p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c])}}return p}('3 0=4.5(6);2(0){2(0.1){0.1.7(0)}};" \
               "',8,8,'el|parentNode|if|var|document|getElementById|\"yt" + str(
            rand) + "\"|removeChild'.split('|'),0,{}))\n//]]>"
        if headers.get('Referer', '') == '':
            body = 'yta = {}'
        return web.Response(body=body, content_type='application/x-javascript', charset='utf-8')

    async def post(self):
        headers = self.request.headers
        post = await self.request.post()
        guid = post.get('guid', self.request.query.get('guid'))
        request = post.get('request', self.request.query.get('request'))
        rand = post.get('rand', self.request.query.get('rand', ''))
        print(guid, request, rand)
        if headers.get('Referer', '') != '' and self.request.is_xml_http:
            pass
        resp_data = {'status': self.request.is_xml_http}
        return web.json_response(resp_data)
