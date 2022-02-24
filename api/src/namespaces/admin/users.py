import sqlalchemy

from flask_restx import Namespace, Resource, fields
from flask import request

from src.models import User, db

from src.decorators.auth import admin_verify
from src.utils.paginate import paginate
from src.swagger.users import user_model, expect_user_model
from src.swagger.paginate import paginate_model


users = Namespace("Admin users", "Admin users routes")


model = user_model(users)

list_model = paginate_model(users, model)

expect_model = expect_user_model(users)


@users.route("/")
class Index(Resource):
    @users.doc("List users")
    @users.marshal_list_with(list_model)
    @admin_verify(users)
    def get(self):
        args = request.args
        page = args.get("page")
        per_page = args.get("per_page")

        return paginate(User, page, per_page)

    @users.doc("Create user")
    @users.expect(model)
    @admin_verify(users)
    def post(self):
        req = request.get_json()

        user = User(
            name=req["name"],
            surname=req["surname"],
            email=req["email"],
            password=req["password"],
            role=req["role"],
        )

        try:
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return "Email already exists", 400

        return "User registered", 201


@users.route("/<int:id>")
@users.param("id", "User identifier")
@users.response(404, "User not found")
class Id(Resource):
    @users.doc("Find user")
    @users.marshal_with(model)
    @admin_verify(users)
    def get(self, id):
        user = User.query.filter_by(id=id).first()

        return user.format()

    @users.doc("Update user")
    @admin_verify(users)
    def put(self, id):
        req = request.get_json()
        user = User.query.filter_by(id=id).first()

        if "name" in req:
            user.name = req["name"]
        if "surname" in req:
            user.surname = req["surname"]
        if "email" in req:
            user.email = req["email"]

        db.session.add(user)
        db.session.commit()

        return "User updated", 200

    @users.doc("Delete user")
    @admin_verify(users)
    def delete(self, id):
        user = User.query.filter_by(id=id).first()

        db.session.delete(user)
        db.session.commit()

        return "User deleted", 200
