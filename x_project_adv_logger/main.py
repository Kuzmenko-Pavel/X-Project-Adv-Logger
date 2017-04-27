import argparse
import asyncio
import logging
import sys

from aiohttp import web
from trafaret_config import commandline

# from aiohttpdemo_polls.db import close_pg, init_pg
from .middlewares import setup_middlewares
from .routes import setup_routes
from .utils import TRAFARET


def init(loop, argv):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(ap,
                                          default_config='./conf.yaml')
    #
    # define your command-line arguments here
    #
    options = ap.parse_args(argv)

    config = commandline.config_from_options(options, TRAFARET)

    # setup application and extensions
    app = web.Application(loop=loop)

    # load config from yaml file in current dir
    app['config'] = config

    # setup views and routes
    setup_routes(app)
    setup_middlewares(app)

    return app


def main(argv):
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()

    app = init(loop, argv)
    web.run_app(app,
                host=app['config']['host'],
                port=app['config']['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
