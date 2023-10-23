#!/usr/bin/env python
"""aioSFTP.

    Create an FTP Server for upload files with integrated watchdogs and security.
See:
https://github.com/phenobarbital/aiosftp
"""
import ast
from os import path
from setuptools import find_packages, setup


def get_path(filename):
    return path.join(path.dirname(path.abspath(__file__)), filename)


def readme():
    with open(get_path('README.md'), 'r', encoding='utf-8') as rd:
        return rd.read()


version = get_path('aiosftp/version.py')
with open(version, 'r', encoding='utf-8') as meta:
    t = compile(meta.read(), version, 'exec', ast.PyCF_ONLY_AST)
    for node in (n for n in t.body if isinstance(n, ast.Assign)):
        if len(node.targets) == 1:
            name = node.targets[0]
            if isinstance(name, ast.Name) and \
                name.id in (
                    '__version__',
                    '__title__',
                    '__description__',
                    '__author__',
                    '__license__', '__author_email__'):
                v = node.value
                if name.id == '__version__':
                    __version__ = v.s
                if name.id == '__title__':
                    __title__ = v.s
                if name.id == '__description__':
                    __description__ = v.s
                if name.id == '__license__':
                    __license__ = v.s
                if name.id == '__author__':
                    __author__ = v.s
                if name.id == '__author_email__':
                    __author_email__ = v.s

setup(
    name=__title__,
    version=__version__,
    python_requires=">=3.8.0",
    url='https://github.com/phenobarbital/aiosftp',
    description=__description__,
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords = "ftp, ftp server, sftp server, ssh server, asyncio",
    license=__license__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Object Brokering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Networking',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: AsyncIO'
    ],
    author='Jesus Lara',
    author_email='jesuslara@phenobarbital.info',
    packages=find_packages(exclude=["contrib", "docs", "tests", "settings"]),
    include_package_data=True,
    setup_requires=[
        'wheel==0.40.0',
        'cython==0.29.33'
    ],
    install_requires=[
        'wheel==0.40.0',
        "aiohttp>=3.8.5",
        "asyncio==3.4.3",
        "asyncdb>=2.2.0",
        "navconfig[default]>=1.1.0",
        "aioftp==0.21.4",
        "siosocks>=0.3.0",
        "asyncssh==2.13.2",
    ],
    extras_require={
        "uvloop": [
            "uvloop>=0.17.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'aioftp = aiosftp.__main__:main'
        ]
    },
    project_urls={  # Optional
        'Source': 'https://github.com/phenobarbital/aiosftp',
        'Funding': 'https://paypal.me/phenobarbital',
        'Say Thanks!': 'https://saythanks.io/to/phenobarbital',
    },
)
