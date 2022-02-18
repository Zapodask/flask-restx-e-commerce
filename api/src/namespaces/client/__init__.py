from flask import Blueprint
from flask_restx import Api

from .products import products


blueprint = Blueprint("client", __name__)
client = Api(blueprint)

# Namespaces
client.add_namespace(products)
