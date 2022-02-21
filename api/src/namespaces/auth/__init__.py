from flask_restx import Api

from .routes import auth as routes


def authNamespaces(api: Api):
    api.add_namespace(routes)
