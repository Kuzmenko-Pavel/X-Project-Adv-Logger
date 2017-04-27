import argparse
import asyncio
import logging
import sys

from aiohttp import web
from trafaret_config import commandline

from .db import init_db
from .middlewares import setup_middlewares
from .routes import setup_routes
from .signal import on_startup
from .utils import TRAFARET_CONF


def init(loop, argv):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(ap,
                                          default_config='./conf.yaml')
    #
    # define your command-line arguments here
    #
    options = ap.parse_args(argv)

    config = commandline.config_from_options(options, TRAFARET_CONF)

    app = web.Application(loop=loop)

    app['config'] = config
    init_db(app)

    on_startup(app)
    setup_routes(app)
    setup_middlewares(app)

    return app


def main(argv):
    log = logging.getLogger('aiohttp')
    log.setLevel(logging.DEBUG)

    f = logging.Formatter('[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(f)
    log.addHandler(ch)

    loop = asyncio.get_event_loop()

    app = init(loop, argv)
    app['log'] = log
    web.run_app(app,
                host=app['config']['host'],
                port=app['config']['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
