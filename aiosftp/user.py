"""User.

UserModel for FTP Users.
"""
import uuid
import hashlib
import base64
import secrets
from asyncdb.models import Model, Column
from datetime import datetime


def at_now():
    return datetime.now()

class FTPUser(Model):
    userid: uuid.UUID = Column(required=False, primary_key=True, db_default='auto')
    username: str = Column(required=False)
    tenant: str = Column(required=False)
    password: str = Column(required=False)
    name: str = Column(required=False)
    last_login: datetime = Column(required=False, default=at_now)
    date_joined: datetime = Column(required=False)
    last_ip: str = Column(required=False)
    is_active: bool = Column(required=False, default=False)

    def validate_password(self, password) -> bool:
        try:
            algorithm, iterations, salt, hash = str(self.password).split("$", 3)
            assert algorithm == 'pbkdf2_sha256'
        except Exception:
            raise Exception(
                f'FTP Users: Invalid password Hash or scheme for user: {self.name}'
            )
        compare_hash = self.create_password(
            password,
            iterations=int(iterations),
            salt=salt,
            token_num=6
        )
        if secrets.compare_digest(self.password, compare_hash):
            return True
        return False

    def create_password(
        self,
        password: str,
        token_num: int = 6,
        iterations: int = 80000,
        salt: str = None
    ):
        if not salt:
            salt = secrets.token_hex(token_num)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations,
            dklen=32,
        )
        strhash = base64.b64encode(key).decode("utf-8").strip()
        return f"pbkdf2_sha256${iterations}${salt}${strhash}"

    class Meta:
        driver = 'pg'
        name = 'ftpusers'
        schema = 'public'
        strict = True
        frozen = False
