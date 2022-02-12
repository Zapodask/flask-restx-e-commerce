import sqlalchemy

from flask_restx import Namespace, Resource, fields
from flask import request


from src.models import Users, db

users = Namespace("users", "Users namespace")


model = users.model(
    "User",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String(required=True),
        "surname": fields.String(required=True),
        "email": fields.String(required=True),
    },
)

expect_model = users.clone(
    "User",
    model,
    {
        "password": fields.String(required=True),
    },
)


@users.route("/")
class Index(Resource):
    @users.doc("List users")
    @users.marshal_list_with(model)
    def get(self):
        response = Users.query.all()
        users = [res.format() for res in response]

        return users

    @users.doc("Create user")
    @users.expect(model)
    def post(self):
        req = request.get_json()

        user = Users(
            name=req["name"],
            surname=req["surname"],
            email=req["email"],
            password=req["password"],
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
    def get(self, id):
        user = Users.query.filter_by(id=id).first()

        return user.format()

    @users.doc("Update user")
    def put(self, id):
        req = request.get_json()
        user = Users.query.filter_by(id=id).first()

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
    def delete(self, id):
        user = Users.query.filter_by(id=id).first()

        db.session.delete(user)
        db.session.commit()

        return "User deleted", 200
