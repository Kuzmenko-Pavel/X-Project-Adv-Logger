from aiohttp import web


class BlockView(web.View):
    async def get(self):
        return web.Response(text='g',
                            headers={
                                "X-Custom-Server-Header": "Custom data",
                            })

    async def post(self):
        return web.Response(text='p',
                            headers={
                                "X-Custom-Server-Header": "Custom data",
                            })
