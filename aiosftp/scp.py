"""SCP

SCP/sFTP Server implemented in Asyncio.
Asyncssh Server.
"""
import os
import ssl
import socket
import asyncio
from datetime import datetime
import asyncssh
from navconfig.logging import logging
from asyncdb import AsyncDB
from .conf import (
    default_dsn,
    SSH_SERVER_HOST,
    SSH_SERVER_PORT,
    SERVICE_BASE_PATH,
    SSL_CERT,
    SSL_KEY,
    CERT_CHECK_HOSTNAME,
    ECDSA_KEY,
    RSA_KEY,
    SSH_KNOWN_HOSTS,
    SSHD_CONFIG,
)
from .user import FTPUser

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(
    certfile=SSL_CERT,
    keyfile=SSL_KEY
)
ctx.options |= ssl.OP_NO_TLSv1
ctx.options |= ssl.OP_NO_TLSv1_1
ctx.options |= ssl.OP_SINGLE_DH_USE
ctx.options |= ssl.OP_SINGLE_ECDH_USE
ctx.check_hostname = CERT_CHECK_HOSTNAME
ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')

asyncssh.set_debug_level(1)
asyncssh.set_log_level(logging.INFO)
logging.basicConfig(level='INFO')

try:
    DEFAULT_HOST = SSH_SERVER_HOST
except Exception as e:
    DEFAULT_HOST = socket.gethostbyname(socket.gethostname())


class aioSSHServer(asyncssh.SSHServer):
    def connection_made(self, conn):
        self.connection = conn
        self.ip = conn.get_extra_info('peername')[0]
        print(f'{self.ip} - Connection received')

    def connection_lost(self, exc):
        print(f'{self.ip} - Connection closed {exc}')
        if exc is not None:
            logging.exception(exc)

    async def begin_auth(self, username: str) -> bool:
        """Handle client authentication request"""
        logging.debug(
            f'sFTP: Starting authentication for user: {username}'
        )
        return True

    def password_auth_supported(self):
        """Return whether or not password authentication is supported."""
        return True

    def kbdint_auth_supported(self):
        return False

    def public_key_auth_supported(self):
        """Return whether or not public key authentication is supported"""
        return False

    async def validate_password(self, username, password):
        try:
            db = AsyncDB('pg', dsn=default_dsn)
            async with await db.connection() as conn:
                FTPUser.Meta.set_connection(conn)
                user = await FTPUser.get(username=username)
                if user.validate_password(password):
                    try:
                        user.last_ip = self.ip
                        user.last_login = datetime.now()
                        await user.update()
                        self.connection.set_extra_info(user=user)
                    except Exception as err:
                        logging.error(err)
                    return True
                else:
                    return False
        except Exception as err:
            logging.exception(
                f"sFTP: Cannot connect with user Subsystem {err}"
            )
            return False

    def auth_completed(self, **kwargs) -> None:
        """Authentication was completed successfully."""
        return True


class aioSFTPServer(asyncssh.SFTPServer):
    def __init__(self, chan: asyncssh.SSHServerChannel):
        root = SERVICE_BASE_PATH
        try:
            user = chan.get_extra_info('user')
            tenant = user.tenant
            if tenant:
                root = SERVICE_BASE_PATH.joinpath(tenant)
        except Exception as err:
            logging.error(err)
        if not root.exists():
            # create automatically
            root.mkdir(exist_ok=True, parents=True)
        logging.debug(
            f'Connecting to Directory: {root}'
        )
        super().__init__(chan, chroot=str(root))


class SCPServer(object):
    """aio sFTP server.

    Attributes:
        host: Hostname of the server.
        port: Port number of the server.
        loop: Event loop to run in.
        kwargs: are passed directly to asyncssh server.
    """
    _server: asyncssh.SFTPServer = None

    def __init__(
            self,
            host: str = DEFAULT_HOST,
            port: int = SSH_SERVER_PORT,
            path: str = SERVICE_BASE_PATH,
            event_loop: asyncio.AbstractEventLoop = None,
            debug: bool = False,
            **kwargs
    ):
        self.host = host
        self.port = port
        self.path = path
        self.debug = debug
        if self.debug is True:
            asyncssh.set_debug_level(1)
            asyncssh.set_log_level(logging.DEBUG)
        self.log = logging.getLogger("aio.ssh")
        self.ssh_key = ECDSA_KEY
        if not self.ssh_key.exists():
            self.ssh_key = RSA_KEY
        self.ssh_config = SSHD_CONFIG
        self.ssh_host_keys = asyncssh.read_private_key_list(self.ssh_key)
        self._known_hosts = SSH_KNOWN_HOSTS
        if self.debug:
            dbg = logging.DEBUG
            asyncssh.set_log_level(dbg)
            asyncssh.set_debug_level(1)
            asyncssh.set_sftp_log_level(1)
            logging.basicConfig(
                level=dbg,
                format="%(asctime)s [%(name)s] %(message)s",
                datefmt="[%H:%M:%S]:",
            )
            self.log.setLevel(dbg)
        if not event_loop:
            self._loop = asyncio.get_event_loop()
            asyncio.set_event_loop(self._loop)
        else:
            self._loop = event_loop
        try:
            os.chdir(str(self.path))
            print(f"SSH: Working Directory: {os.getcwd()}")
        except Exception as err:
            print(err)
            raise

    async def close(self):
        """Close.
        Closing FTP server connections
        """
        try:
            self.log.info('::: aio-sFTP: Closing all sFTP connections.')
            self._server.close()
        except Exception as err:
            logging.exception(err)

    def handle_clients(self, process: asyncssh.SSHServerProcess) -> None:
        user = process.get_extra_info('username')
        process.stdout.write(f'Hi {user}, Welcome to aioSFTP SSH server\n')

    async def start(self):
        """Starts server."""
        # Serve requests until Ctrl+C is pressed
        self.log.info(
            f'::: aio-sFTP: Serving sFTP Server {self.host} on {self.port}'
        )
        # running forever
        self._server = await asyncssh.listen(
            server_factory=aioSSHServer,
            sftp_factory=aioSFTPServer,
            process_factory=self.handle_clients,
            host=self.host,
            port=int(self.port),
            server_host_keys=[self.ssh_key],
            family=socket.AF_INET,
            allow_scp=True,
            password_auth=True,
            host_based_auth=True,
            known_client_hosts=[self._known_hosts],
            config=str(self.ssh_config)
        )
        # print('sFTP Server: ', self._server)
