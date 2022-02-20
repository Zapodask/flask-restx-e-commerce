from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt_identity

from src.models import Users, db

from src.decorators.auth import auth_verify
from src.utils.findOne import findOne


profile = Namespace("profile", "Profile namespace")

model = profile.model(
    "User",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "surname": fields.String(),
        "email": fields.String(),
    },
)

expect_update_informations_model = profile.model(
    "Expect change informations",
    {
        "name": fields.String(),
        "surname": fields.String(),
    },
)

expect_change_password_model = profile.model(
    "Expect change password",
    {
        "password": fields.String(required=True),
        "new_password": fields.String(required=True),
        "new_password_confirmation": fields.String(required=True),
    },
)


@profile.route("/")
class Index(Resource):
    @profile.doc(
        responses={
            400: {"User not found"},
        },
    )
    @profile.marshal_with(model)
    @auth_verify(profile)
    def get(self):
        id = get_jwt_identity()

        user = findOne(profile, Users, id)

        return user.format()

    @profile.doc(
        body=expect_update_informations_model,
        responses={
            200: {"Success"},
            400: {"User not found"},
        },
    )
    @auth_verify(profile)
    def put(self):
        id = get_jwt_identity()
        req = request.get_json()

        user = findOne(profile, Users, id)

        if "name" in req:
            user.name = req["name"]

        if "surname" in req:
            user.surname = req["surname"]

        db.session.add(user)
        db.session.commit()

        return {"message": "Updated informations"}


@profile.route("/change-password")
class ChangePassword(Resource):
    @profile.doc(
        body=expect_change_password_model,
        responses={
            200: {"Success"},
            400: {"User not found"},
            400: {"Invalid password"},
            400: {"New password not match"},
        },
    )
    @auth_verify(profile)
    def put(self):
        id = get_jwt_identity()
        req = request.get_json()

        user = findOne(profile, Users, id)

        if not user.check_password(req["password"]):
            return {"message": "Invalid password"}, 400

        if not req["new_password"] == req["new_password_confirmation"]:
            return {"message": "Invalid new password confirmation"}, 400

        user.hash_password(req["new_password"])

        db.session.add(user)
        db.session.commit()

        return {"message": "Password changed"}
