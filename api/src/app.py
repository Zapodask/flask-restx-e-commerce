from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .models import db
from .services.mail import mail

from .users.namespace import users
from .auth.namespace import auth


app = Flask(__name__)
app.config.from_object("src.config.Config")
CORS(app)
api = Api(app)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
mail.init_app(app)

# Namespaces
api.add_namespace(users)
api.add_namespace(auth)
