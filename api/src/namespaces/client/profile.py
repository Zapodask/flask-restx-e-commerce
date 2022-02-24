from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt_identity

from src.models import User, db

from src.decorators.auth import auth_verify
from src.utils.findOne import findOne
from src.swagger.users import user_model
from src.swagger.profile import (
    expect_update_profile_model,
    expect_change_password_model,
)


profile = Namespace("Profile", "Profile routes", path="/profile")

model = user_model(profile)

expect_update = expect_update_profile_model(profile)

expect_change_password = expect_change_password_model(profile)


@profile.route("/")
@profile.response(404, "User not found")
class Index(Resource):
    @profile.doc("Get profile")
    @profile.marshal_with(model)
    @auth_verify(profile)
    def get(self):
        id = get_jwt_identity()

        user = findOne(User, id)

        return user.format()

    @profile.doc("Update informations")
    @profile.expect(expect_update)
    @profile.response(200, "Success")
    @auth_verify(profile)
    def put(self):
        id = get_jwt_identity()
        req = request.get_json()

        user = findOne(User, id)

        if "name" in req:
            user.name = req["name"]

        if "surname" in req:
            user.surname = req["surname"]

        db.session.add(user)
        db.session.commit()

        return {"message": "Updated informations"}


@profile.route("/change-password")
class ChangePassword(Resource):
    @profile.doc("Change password")
    @profile.response(200, "Success")
    @profile.response(404, "User not found")
    @profile.response(400, "Invalid password")
    @profile.response(400, "New password not match")
    @profile.expect(expect_change_password)
    @auth_verify(profile)
    def put(self):
        id = get_jwt_identity()
        req = request.get_json()

        user = findOne(User, id)

        if not user.check_password(req["password"]):
            return {"message": "Invalid password"}, 400

        if not req["new_password"] == req["new_password_confirmation"]:
            return {"message": "Invalid new password confirmation"}, 400

        user.hash_password(req["new_password"])

        db.session.add(user)
        db.session.commit()

        return {"message": "Password changed"}
