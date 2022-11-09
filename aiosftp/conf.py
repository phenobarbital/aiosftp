"""
aioSFTP Configuration.
"""
# Import Config Class
from pathlib import Path
from navconfig import config, BASE_DIR

"""
Databases
"""
# DB Default
# POSTGRESQL Default
DBHOST = config.get('DBHOST', fallback='localhost')
DBUSER = config.get('DBUSER')
DBPWD = config.get('DBPWD')
DBNAME = config.get('DBNAME', fallback='navigator')
DBPORT = config.get('DBPORT', fallback=5432)
if not DBUSER:
    raise Exception('Missing PostgreSQL Default Settings.')

# database for changes (admin)
default_dsn = 'postgres://{user}:{password}@{host}:{port}/{db}'.format(
    user=DBUSER,
    password=DBPWD,
    host=DBHOST,
    port=DBPORT,
    db=DBNAME
)


"""
FTP Server
"""
FTP_ENABLED = config.getboolean('ENABLE_FTP', fallback=False)
# main config for FTP:
FTP_SERVER_HOST = config.get('FTP_SERVER_HOST', fallback='127.0.0.1')
FTP_SERVER_PORT = config.getint('FTP_SERVER_PORT', fallback=2122)

"""
SSH Server
"""
SSH_ENABLED = config.getboolean('ENABLE_SSH', fallback=False)

SSH_SERVER_HOST = config.get('SSH_SERVER_HOST', fallback='127.0.0.1')
SSH_SERVER_PORT = config.getint('SSH_SERVER_PORT', fallback=8384)

## path for serving files
SERVICE_BASE_PATH = Path(config.get('SERVICE_BASE_PATH', fallback=BASE_DIR))

### Secure Connections
SSL_CERT = config.get('SFTP_SSL_CERT', fallback='docs/ssl/ssl-cert-snakeoil.pem')
SSL_KEY = config.get('SFTP_SSL_KEY', fallback='docs/ssl/ssl-cert-snakeoil.key')
CERT_CHECK_HOSTNAME = config.get('SFTP_SSL_CHECK_HOSTNAME', fallback=False)

ECDSA_KEY = config.get('ECDSA_KEY', fallback=BASE_DIR.joinpath('docs', 'ssl', 'ssh_host_ecdsa_key'))
RSA_KEY = config.get('RSA_KEY', fallback=BASE_DIR.joinpath('docs', 'ssl', 'ssh_host_rsa_key'))

### SSH Configuration
SSHD_CONFIG = config.get('SSHD_CONFIG', fallback=BASE_DIR.joinpath('docs', 'ssl', 'sshd_config'))
SSH_KNOWN_HOSTS = config.get('SSH_KNOWN_HOSTS', fallback=BASE_DIR.joinpath('docs', 'ssl', 'known_hosts'))

try:
    from settings.settings import * # pylint: disable=W0614,W0401
except ImportError as ex:
    print(ex)
