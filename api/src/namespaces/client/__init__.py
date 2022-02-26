from flask_restx import Api

from .products import products
from .profile import profile
from .orders import orders


def clientNamespaces(api: Api):
    api.add_namespace(products)
    api.add_namespace(profile)
    api.add_namespace(orders)
