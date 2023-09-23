"""FTP
FTP Server implemented in Asyncio.
AioFTP Server.
"""
import os
import ssl
import pathlib
import socket
import asyncio
import uvloop
import aioftp
from aioftp.server import AbstractUserManager, AvailableConnections
from navconfig import BASE_DIR
from navconfig.logging import logging
from .conf import (
    FTP_SERVER_HOST,
    FTP_SERVER_PORT,
    SERVICE_BASE_PATH,
    SSL_CERT,
    SSL_KEY,
    CERT_CHECK_HOSTNAME
)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

try:
    DEFAULT_HOST = FTP_SERVER_HOST
except Exception as e:
    DEFAULT_HOST = socket.gethostbyname(socket.gethostname())


class UserModel(AbstractUserManager):
    path: pathlib.Path = None

    def __init__(self, path, *args, **kwargs):
        self.path = path
        super(UserModel, self).__init__(timeout=10, *args, **kwargs)
        self.available_connections = {}

    async def get_user(self, login: str) -> aioftp.User:
        user = None
        print(login)
        perm = []
        state = None
        info = ''
        perm.append(
            aioftp.Permission('/', readable=True, writable=True)
        )
        # perm.append(
        #     aioftp.Permission(home_path, readable=True, writable=True)
        # )
        user = aioftp.User(
            login=login,
            password=login,
            base_path=self.path,
            home_path=pathlib.PurePosixPath("/"),
            maximum_connections=2,
            permissions=perm
        )
        print(user)
        self.available_connections[user] = AvailableConnections(
            user.maximum_connections)
        if user is None:
            state = AbstractUserManager.GetUserResponse.ERROR
            info = "no such username"
        if self.available_connections[user].locked():
            state = AbstractUserManager.GetUserResponse.ERROR
            info = f"too much connections for {user.login or 'anonymous'!r}"
        elif user.login is None:
            state = AbstractUserManager.GetUserResponse.ERROR
            info = "Anonymous login prohibited"
        elif user.password is None:
            state = AbstractUserManager.GetUserResponse.PASSWORD_REQUIRED
            info = "Password required"
        else:
            state = AbstractUserManager.GetUserResponse.OK
            info = 'User OK'
        print(state, user, info)
        # if state != AbstractUserManager.GetUserResponse.ERROR:
        #     self.available_connections[user].acquire()
        return state, user, info

    async def authenticate(self, user: aioftp.User, password: str) -> bool:
        print(user, password)
        return True

    async def notify_logout(self, user: aioftp.User):
        print(user)
        self.available_connections[user].release()
        return user


class FTPServer(object):
    """aio FTP server.

    Attributes:
        host: Hostname of the server.
        port: Port number of the server.
        loop: Event loop to run in.
        kwargs: are passed directly to aioftp server.
    """
    _server: aioftp.Server = None

    def __init__(
            self,
            host: str = DEFAULT_HOST,
            port: int = FTP_SERVER_PORT,
            path: str = SERVICE_BASE_PATH,
            event_loop: asyncio.AbstractEventLoop = None,
            debug: bool = False,
            users: list = None,
            **kwargs
    ):
        self.host = host
        self.port = port
        self.path = path
        self.debug = debug
        self.log = logging.getLogger("aio.ftp")
        self.ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.ssl_ctx.load_cert_chain(
            certfile=str(
                BASE_DIR.joinpath(SSL_CERT)
            ),
            keyfile=str(
                BASE_DIR.joinpath(SSL_KEY)
            )
        )
        self.ssl_ctx.options |= ssl.OP_NO_TLSv1
        self.ssl_ctx.options |= ssl.OP_NO_TLSv1_1
        self.ssl_ctx.options |= ssl.OP_SINGLE_DH_USE
        self.ssl_ctx.options |= ssl.OP_SINGLE_ECDH_USE
        self.ssl_ctx.check_hostname = CERT_CHECK_HOSTNAME
        self.ssl_ctx.verify_mode = ssl.VerifyMode.CERT_NONE
        self.ssl_ctx.set_ciphers(
            'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')

        if self.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s [%(name)s] %(message)s",
                datefmt="[%H:%M:%S]:",
            )
            self.log.setLevel(logging.DEBUG)
        if not event_loop:
            self._loop = asyncio.get_event_loop()
            asyncio.set_event_loop(self._loop)
        else:
            self._loop = event_loop
        try:
            os.chdir(str(self.path))
            print(f"FTP: Working Directory: {os.getcwd()}")
            users = UserModel(self.path)
            self._server = aioftp.Server(
                users=users,
                path_io_factory=aioftp.AsyncPathIO,
                socket_timeout=30,
                idle_timeout=60,
                path_timeout=10,
                encoding='utf-8',
                maximum_connections=10,
                ssl=self.ssl_ctx
            )
        except Exception as err:
            print(err)
            raise

    async def close(self):
        """Close.
        Closing FTP server connections
        """
        try:
            await self._server.close()
            self.log.info('::: aio-FTP: Closing all FTP connections.')
        except Exception as err:
            logging.exception(err)

    async def start(self):
        """Starts server."""
        # Serve requests until Ctrl+C is pressed
        self.log.info(
            f'::: aio-FTP: Serving FTP Server {self.host} on {self.port}'
        )
        # running forever
        await self._server.start(
            host=self.host,
            port=int(self.port),
            family=socket.AF_INET
            # loop=self._loop
        )
