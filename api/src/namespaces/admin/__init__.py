from flask_restx import Api

from .users import users
from .products import products
from .orders import orders


def adminNamespaces(api: Api):
    api.add_namespace(users, path="/admin/users")
    api.add_namespace(products, path="/admin/products")
    api.add_namespace(orders, path="/admin/orders")
