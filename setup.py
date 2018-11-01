import os
import re

from setuptools import setup, find_packages


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'x_project_adv_logger', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = 'Cannot find version in x_project_adv_logger/__init__.py'
            raise RuntimeError(msg)


install_requires = ['aiohttp',
                    'aiodns',
                    'async-timeout',
                    'multidict',
                    'pymongo',
                    'motor',
                    'ujson',
                    'trafaret-config',
                    'uvloop',
                    'cchardet',
                    'pytz',
                    'aiojobs']

setup(
    name="X-Project-Adv-Logger",
    version=read_version(),
    url="",
    packages=find_packages(),
    package_data={

    },
    install_requires=install_requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
        ],
    }
)
