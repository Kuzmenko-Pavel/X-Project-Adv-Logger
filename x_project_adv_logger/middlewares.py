import time

from aiohttp import web

from x_project_adv_logger.logger import logger, exception_message


async def handle_404(request, response):
    return web.Response(text='')


async def handle_403(request, response):
    return web.Response(text='')


async def handle_405(request, response):
    return web.Response(text='')


async def handle_500(request, response):
    return web.Response(text='')


def error_pages(overrides):
    async def middleware(app, handler):
        async def middleware_handler(request):
            try:
                request.start_time = time.time()
                response = await handler(request)
                override = overrides.get(response.status)
                if override is None:
                    return response
                else:
                    return await override(request, response)
            except web.HTTPException as ex:
                if ex.status == 404:
                    logger.info(exception_message(exc=str(ex), request=str(request.message)))
                elif ex.status == 403:
                    logger.warning(exception_message(exc=str(ex), request=str(request.message)))
                else:
                    logger.error(exception_message(exc=str(ex), request=str(request.message)))

                override = overrides.get(ex.status)
                if override is None:
                    raise
                else:
                    return await override(request, ex)

        return middleware_handler

    return middleware


def setup_middlewares(app):
    error_middleware = error_pages({404: handle_404,
                                    405: handle_405,
                                    500: handle_500})
    app.middlewares.append(error_middleware)
