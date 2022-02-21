from flask_restx import fields, Namespace


def expect_login_model(ns: Namespace):
    ns.model(
        "Expect login",
        {
            "email": fields.String(required=True),
            "password": fields.String(required=True),
        },
    )


def expect_change_password_model(ns: Namespace):
    ns.model(
        "Expect change password",
        {
            "password": fields.String(required=True),
            "new_password": fields.String(required=True),
            "new_password_confirmation": fields.String(required=True),
        },
    )
