from os import getenv
from datetime import timedelta


stage = getenv("STAGE")


class Config(object):
    # Sqlalchemy
    SQLALCHEMY_DATABASE_URI = "postgresql://{0}:{1}@{2}/{3}".format(
        getenv("DB_USER"),
        getenv("DB_PASS"),
        f"{stage}-postgres" if stage else "localhost",
        getenv("DB_NAME"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Jwt
    SECRET_KEY = getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    # Flask-mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = getenv("MAIL_USERNAME")
