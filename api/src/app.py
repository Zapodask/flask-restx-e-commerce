from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .models import db
from .services.mail import mail

from .namespaces.client import blueprint as client
from .namespaces.admin import blueprint as admin
from .namespaces.auth import blueprint as auth


app = Flask(__name__)
app.config.from_object("src.config.Config")
CORS(app)
api = Api(app)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
mail.init_app(app)

# Blueprints
app.register_blueprint(client)
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(admin, url_prefix="/admin")
