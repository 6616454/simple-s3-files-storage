from aioboto3 import Session


class S3Repository:
    def __init__(self, session: Session, s3_host: str, user: str, password: str):
        self.session = session
        self.s3_host = s3_host
        self.user = user
        self.password = password
