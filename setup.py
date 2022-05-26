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


install_requires = ['aiohttp==2.3.10',
                    'aiodns==2.0.0',
                    'async-timeout==2.0.1',
                    'multidict==4.7.5',
                    'pymongo==3.10.1',
                    'motor==2.1.0',
                    'ujson==5.2.0',
                    'trafaret==2.0.2',
                    'trafaret-config==2.0.2',
                    'uvloop==0.14.0',
                    'cchardet==2.1.6',
                    'chardet==3.0.4',
                    'pytz==2019.3',
                    'aiojobs==0.2.1']

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
