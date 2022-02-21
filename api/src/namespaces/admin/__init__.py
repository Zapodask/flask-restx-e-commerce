from flask_restx import Api

from .users import users
from .products import products


def adminNamespaces(api: Api):
    api.add_namespace(users, path="/admin/users")
    api.add_namespace(products, path="/admin/products")
