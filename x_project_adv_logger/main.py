import argparse
import asyncio
import os
import sys

try:
    from http.cookies import Morsel

    Morsel._reserved['samesite'] = 'SameSite'
except Exception:
    pass

import uvloop
from aiohttp import web
from aiojobs.aiohttp import setup as aiojobs_setup
from trafaret_config import commandline

from x_project_adv_logger.db import init_db, close_db
from x_project_adv_logger.logger import logger
from x_project_adv_logger.middlewares import setup_middlewares
from x_project_adv_logger.routes import setup_routes
from x_project_adv_logger.utils import TRAFARET_CONF

uvloop.install()

def init(loop, argv):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ap = argparse.ArgumentParser(description='Great Description To Be Here')
    ap.add_argument('-s', "--socket", action='store', dest='socket', help='unix socket')
    commandline.standard_argparse_options(ap.add_argument_group('configuration'),
                                          default_config=dir_path + '/../conf.yaml')
    #
    # define your command-line arguments here
    #
    options = ap.parse_args(argv)
    config = commandline.config_from_options(options, TRAFARET_CONF)
    config['socket'] = options.socket
    app = web.Application(loop=loop)
    app['config'] = config
    setup_routes(app)
    setup_middlewares(app)
    aiojobs_setup(app)
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    return app


def main(argv):
    loop = asyncio.get_event_loop()
    app = init(loop, argv)
    app['log'] = logger
    if app['config']['socket']:
        os.makedirs(os.path.dirname(app['config']['socket']), exist_ok=True)
        web.run_app(app, path=app['config']['socket'], backlog=1024, access_log=None)
    else:
        web.run_app(app, host=app['config']['host'], port=app['config']['port'], backlog=1024, access_log=None)


if __name__ == '__main__':
    main(sys.argv[1:])
