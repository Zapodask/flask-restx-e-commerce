from flask import Blueprint
from flask_restx import Api

from .users import users
from .products import products


blueprint = Blueprint("admin", __name__)
admin = Api(blueprint)

# Namespaces
admin.add_namespace(users)
admin.add_namespace(products)
