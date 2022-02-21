from flask_restx import Api

from .products import products
from .profile import profile


def clientNamespaces(api: Api):
    api.add_namespace(products)
    api.add_namespace(profile)
