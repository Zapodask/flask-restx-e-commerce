import os

from flask_restx import Namespace, Resource, fields
from flask import render_template, request
from flask_jwt_extended import create_access_token, get_jwt_identity, decode_token
from flask_mail import Message
from datetime import timedelta

from src.models import Users, db
from src.decorators.auth import auth_verify
from src.services.mail import mail


auth = Namespace("auth", "Auth namespace")

expect_login_model = auth.model(
    "Expect login",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

expect_change_password_model = auth.model(
    "Expect change password",
    {
        "password": fields.String(required=True),
        "new_password": fields.String(required=True),
        "new_password_confirmation": fields.String(required=True),
    },
)


@auth.route("/login")
class Login(Resource):
    @auth.doc("Login")
    @auth.expect(expect_login_model)
    def post(self):
        req = request.get_json()

        user = Users.query.filter_by(email=req["email"]).first()

        if not user.check_password(req["password"]):
            return {"message": "Invalid email or password"}, 401

        access_token = create_access_token(user.id)

        return {"token": access_token}


@auth.route("/change-password")
class ChangePassword(Resource):
    @auth.doc("Change password")
    @auth.expect(expect_change_password_model)
    @auth_verify(auth)
    def put(self):
        id = get_jwt_identity()
        req = request.get_json()

        user = Users.query.filter_by(id=id).first()

        if not user.check_password(req["password"]):
            return {"message": "Invalid password"}, 400

        if not req["new_password"] == req["new_password_confirmation"]:
            return {"message": "Invalid new password confirmation"}, 400

        user.hash_password(req["new_password"])

        db.session.add(user)
        db.session.commit()

        return {"message": "Password changed"}, 200


@auth.route("/forgot-password")
class ChangeEmail(Resource):
    def post(self):
        req = request.get_json()

        try:
            user = Users.query.filter_by(email=req["email"]).first()

            msg = Message(
                subject="Forgot your password?",
                recipients=[user.email],
            )

            expires_in = timedelta(minutes=30)
            token = create_access_token(user.email, expires_delta=expires_in)

            msg.html = render_template(
                "emails/forgot-password.html",
                front_url=os.getenv("FRONT_URL"),
                token=token,
            )

            mail.send(msg)
        finally:
            return {
                "message": "A recovery email has been sent if the email is registered"
            }

    def put(self):
        req = request.get_json()

        email = decode_token(req["token"])["sub"]

        user = Users.query.filter_by(email=email).first()

        if req["new_password"] == req["new_password_confirmation"]:
            user.password = req["new_password"]
        else:
            return {"message": "Invalid new password confirmation"}, 400

        return {"message": "Password changed"}
