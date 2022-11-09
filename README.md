# aioSFTP #

[![pypi](https://img.shields.io/pypi/v/aiosftp?style=plastic)](https://pypi.org/project/aiosftp/)
[![status](https://img.shields.io/pypi/status/aiosftp?style=plastic)](https://pypi.org/project/aiosftp/)
[![versions](https://img.shields.io/pypi/pyversions/blacksheep.svg?style=plastic)](https://github.com/phenobarbital/naiosftp)
[![Apache licensed](https://img.shields.io/github/license/phenobarbital/aiosftp?style=plastic)](https://raw.githubusercontent.com/phenobarbital/aiosftp/master/LICENSE)


aioSFTP is a FTP/sFTP/SSH server implemented on top of asyncio with integrated security, TLS/SSL connections, Users and other cool features.
work with ``asyncio``.

``aioSFTP`` requires Python 3.8+ and is distributed under Apache 2 license.

## Which services are provided ##

* FTP Server (using aioftp)
* sFTP server and SSH Server (using asyncssh)
* Web interface for uploading files (using aiohttp)
### How do I get set up? ###

First, you need to install aioSFTP:

.. code-block ::

    pip install aiosftp

Then, you can start the server running the command:

.. code-block ::

   aiosftp --host <hostname> --port <port>

where

- ``<hostname>`` is a hostname of the server (default, listen on localhost)
- ``<port>`` SSH Server Port
- ``<ftp-port>`` FTP Server Port
- ``<path>`` The base path where all files live in.


### License ###

aioSFTP is copyright of Jesus Lara (https://phenobarbital.info) and is under Apache 2 license. I am providing code in this repository under an open source license, remember, this is my personal repository; the license that you receive is from me and not from my employeer.
