from flask_restx import fields, Namespace


def expectUpdateSwagger(ns: Namespace):
    return ns.model(
        "Expect update profile",
        {
            "name": fields.String(),
            "surname": fields.String(),
        },
    )


def expectChangePasswordSwagger(ns: Namespace):
    return ns.model(
        "Expect change password",
        {
            "password": fields.String(required=True),
            "new_password": fields.String(required=True),
            "new_password_confirmation": fields.String(required=True),
        },
    )
