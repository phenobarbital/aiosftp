"""aioSFTP Meta information.
   FTP/SSH Servers implementation.
"""

__title__ = 'aiosftp'
__description__ = ('FTP/SSH/sFTP Server implementation built on to of Asyncio.'
                   'Facility to deploy SSH server easily inside any project.')
__version__ = '0.2.6'
__author__ = 'Jesus Lara'
__author_email__ = 'jesuslara@phenoarbital.info'
__license__ = 'Apache-2'

def get_version() -> tuple:  # pragma: no cover
    """Get aiosftp server version as a tuple.
    """
    return tuple(x for x in __version__.split('.'))  # pragma: no cover
