from os import getenv
from datetime import timedelta


stage = getenv("STAGE")


class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://{0}:{1}@{2}/{3}".format(
        getenv("DB_USER"),
        getenv("DB_PASS"),
        f"{stage}-postgres" if stage else "localhost",
        getenv("DB_NAME"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
