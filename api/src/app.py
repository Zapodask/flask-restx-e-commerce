from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .models import db
from .services.mail import mail

from .namespaces.client import clientNamespaces
from .namespaces.auth import authNamespaces
from .namespaces.admin import adminNamespaces


app = Flask(__name__)
app.config.from_object("src.config.Config")
CORS(app)
api = Api(app, doc="/swagger")

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
mail.init_app(app)

# Namespaces
## Client
clientNamespaces(api)

## Auth
authNamespaces(api)

## Admin
adminNamespaces(api)
