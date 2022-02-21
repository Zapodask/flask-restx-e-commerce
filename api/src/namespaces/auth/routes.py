import os
import sqlalchemy

from flask_restx import Namespace, Resource
from flask import render_template, request
from flask_jwt_extended import create_access_token, decode_token
from flask_mail import Message
from datetime import timedelta

from src.models import Users, db
from src.services.mail import mail
from src.swagger.auth import expect_login_model


auth = Namespace("Auth", "Auth routes", path="/auth")

expect_login = expect_login_model(auth)


@auth.route("/register")
class Register(Resource):
    @auth.doc("Register")
    def post(self):
        req = request.get_json()

        user = Users(
            name=req["name"],
            surname=req["surname"],
            email=req["email"],
            password=req["password"],
            role="client",
        )

        try:
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return "Email already exists", 400

        return "User registered", 201


@auth.route("/login")
class Login(Resource):
    @auth.doc("Login")
    @auth.expect(expect_login)
    def post(self):
        req = request.get_json()

        user = Users.query.filter_by(email=req["email"]).first()

        if not user.check_password(req["password"]):
            return {"message": "Invalid email or password"}, 401

        access_token = create_access_token(user.id)

        return {"token": access_token}


@auth.route("/forgot-password")
class ForgotPassword(Resource):
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
