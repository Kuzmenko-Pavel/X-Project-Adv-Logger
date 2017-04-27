from aiohttp import web


class OfferView(web.View):
    async def post(self):
        return web.Response(text='p',
                            headers={
                                "X-Custom-Server-Header": "Custom data",
                            })
