from flask_restx import fields, Namespace


def expect_update_profile_model(ns: Namespace):
    return ns.model(
        "Expect update profile",
        {
            "name": fields.String(),
            "surname": fields.String(),
        },
    )


def expect_change_password_model(ns: Namespace):
    return ns.model(
        "Expect change password",
        {
            "password": fields.String(required=True),
            "new_password": fields.String(required=True),
            "new_password_confirmation": fields.String(required=True),
        },
    )
