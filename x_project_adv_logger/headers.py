__all__ = ['cookie', 'csp', 'detect_webp', 'xml_http_request', 'cors']
import asyncio
import functools
import time
from datetime import datetime, timedelta
from uuid import uuid4

from aiohttp import web, hdrs
from aiohttp.abc import AbstractView


def cookie(name='yottos_unique_id', domain='.yottos.com', days=365):
    def wrapper(func):
        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(*args):
            expires = datetime.utcnow() + timedelta(days=days)
            user_cookie_expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
            user_cookie_max_age = 60 * 60 * 24 * days
            # Supports class based views see web.View
            if isinstance(args[0], AbstractView):
                request = args[0].request
            else:
                request = args[-1]
            user_cookie = request.cookies.get(name, str(time.time()).replace('.', ''))
            if isinstance(args[0], AbstractView):
                args[0].request.user_cookie = user_cookie
            else:
                args[-1].user_cookie = user_cookie
            if asyncio.iscoroutinefunction(func):
                coro = func
            else:
                coro = asyncio.coroutine(func)
            context = yield from coro(*args)
            if isinstance(context, web.StreamResponse):
                context.set_cookie(name, user_cookie,
                                   expires=user_cookie_expires,
                                   domain=domain,
                                   max_age=user_cookie_max_age)
            return context

        return wrapped

    return wrapper


def csp():
    def wrapper(func):
        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(*args):
            if isinstance(args[0], AbstractView):
                request = args[0].request
            else:
                request = args[-1]
            nonce = uuid4().hex
            request.nonce = nonce
            host = request.host
            csp = []
            csp_data = {
                'base-uri': [host],
                'default-src': [host],
                'img-src': ['data:', 'cdn.yottos.com'],
                'script-src': ["'unsafe-inline'", "'nonce-%s'" % nonce, host],
                'connect-src': [host],
                'style-src': ["'unsafe-inline'"],
                'worker-src': [],
                'frame-src': [],
                'manifest-src': [],
                'media-src': [],
                'font-src': [],
                'child-src': [],
                'form-action': [],
                'object-src': [],
                'sandbox': ['allow-scripts', 'allow-same-origin', 'allow-popups'],
                # 'require-sri-for': ['script', 'style'],

            }
            if request.app['config']['debug']['console']:
                csp_data['style-src'].append("'self'")
                csp_data['img-src'].append("'self'")
            if asyncio.iscoroutinefunction(func):
                coro = func
            else:
                coro = asyncio.coroutine(func)
            context = yield from coro(*args)
            if isinstance(context, web.StreamResponse):
                for key, value in csp_data.items():
                    if len(value) == 0:
                        value.append("'none'")
                    csp.append('%s %s' % (key, ' '.join(value)))
                csp.append('block-all-mixed-content')
                context.headers['content-security-policy'] = '; '.join(csp)
                return context
            return context

        return wrapped

    return wrapper


def detect_webp():
    def wrapper(func):
        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(*args):
            if isinstance(args[0], AbstractView):
                args[0].request.is_not_webp = 'webp' in args[0].request.headers.get('ACCEPT', [])
            else:
                args[-1].is_not_webp = 'webp' in args[-1].headers.get('ACCEPT', [])
            if asyncio.iscoroutinefunction(func):
                coro = func
            else:
                coro = asyncio.coroutine(func)
            context = yield from coro(*args)
            return context

        return wrapped

    return wrapper


def xml_http_request():
    def wrapper(func):
        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(*args):
            if isinstance(args[0], AbstractView):
                request = args[0].request
            else:
                request = args[-1]
            is_xml_http = bool(request.headers.get('X-Requested-With', False))
            if is_xml_http and request.can_read_body:
                if asyncio.iscoroutinefunction(func):
                    coro = func
                else:
                    coro = asyncio.coroutine(func)
                context = yield from coro(*args)
                return context
            else:
                raise web.HTTPForbidden()

        return wrapped

    return wrapper


def cors(allow_origin=None, allow_headers=None):
    def wrapper(func):
        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(*args):
            ao = allow_origin
            ah = allow_headers
            if isinstance(args[0], AbstractView):
                request = args[0].request
            else:
                request = args[-1]

            if ao is None:
                ao = '%s//:%s' % (request.scheme, request.host)
            if ah is None:
                ah = request.method

            if asyncio.iscoroutinefunction(func):
                coro = func
            else:
                coro = asyncio.coroutine(func)
            context = yield from coro(*args)
            if isinstance(context, web.StreamResponse):
                context.headers[hdrs.ACCESS_CONTROL_ALLOW_ORIGIN] = ao
                # context.headers[hdrs.ACCESS_CONTROL_ALLOW_HEADERS] = ah
                # context.headers[hdrs.ACCESS_CONTROL_ALLOW_METHODS] = '%s %s' % (hdrs.METH_GET, hdrs.METH_POST)
                # context.headers[hdrs.ACCESS_CONTROL_ALLOW_CREDENTIALS] = 'true'
            return context
        return wrapped
    return wrapper
