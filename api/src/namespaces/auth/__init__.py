from flask import Blueprint
from flask_restx import Api

from .routes import auth as routes

blueprint = Blueprint("auth", __name__)
auth = Api(blueprint)

auth.add_namespace(routes)
