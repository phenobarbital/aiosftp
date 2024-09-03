"""aio (s)FTP server entry point."""
import asyncio
import argparse
from .ftp import FTPServer
from .scp import SCPServer
from .conf import (
    FTP_SERVER_HOST,
    FTP_SERVER_PORT,
    SSH_SERVER_HOST,
    SSH_SERVER_PORT,
    SERVICE_BASE_PATH
)
from .uv import install_uvloop


install_uvloop()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def main() -> None:
    """Main Worker Function."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--host', dest='host', type=str,
                        default=SSH_SERVER_HOST,
                        help='set server host'
                        )
    parser.add_argument('--port', dest='port', type=int,
                        default=SSH_SERVER_PORT,
                        help='set server port'
                        )
    parser.add_argument('--ftp-host', dest='ftp_host', type=str,
                        default=FTP_SERVER_HOST,
                        help='Set server FTP Host'
                        )
    parser.add_argument('--ftp-port', dest='ftp_port', type=int,
                        default=FTP_SERVER_PORT,
                        help='Set server FTP port'
                        )
    parser.add_argument('--path', dest='path', type=str,
                        default=SERVICE_BASE_PATH,
                        help='Base path for FTP and SSH clients'
                        )
    parser.add_argument('--debug', action="store_true", default=False,
                        help="Start (s)FTP server in Debug Mode"
                        )
    args = vars(parser.parse_args())
    if not args['ftp_host']:
        args['ftp_host'] = args['host']
    print('::: Starting FTP and sFTP Server')
    ftp_args = {
        "host": args['ftp_host'],
        "port": args['ftp_port'],
        "path": args['path'],
        "debug": args['debug'],
    }
    try:
        ftp = FTPServer(**ftp_args, event_loop=loop)
        scp = SCPServer(**args, event_loop=loop)
        loop.run_until_complete(
            ftp.start()
        )
        loop.run_until_complete(
            scp.start()
        )
        loop.run_forever()
    except Exception:
        raise
    except KeyboardInterrupt:
        loop.run_until_complete(ftp.close())
        loop.run_until_complete(scp.close())
        print('Closing (s)FTP Connections ...')
    finally:
        loop.close()


if __name__ == '__main__':
    main()
