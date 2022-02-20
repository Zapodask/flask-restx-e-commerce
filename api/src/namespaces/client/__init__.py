from flask import Blueprint
from flask_restx import Api

from .products import products
from .profile import profile


blueprint = Blueprint("client", __name__)
client = Api(blueprint)

# Namespaces
client.add_namespace(products)
client.add_namespace(profile)
