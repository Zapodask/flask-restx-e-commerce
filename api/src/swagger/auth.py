from flask_restx import fields, Namespace


def expect_register_model(ns: Namespace):
    return ns.model(
        "Expect register",
        {
            "name": fields.String(required=True),
            "surname": fields.String(required=True),
            "email": fields.String(required=True),
            "password": fields.String(required=True),
        },
    )


def expect_login_model(ns: Namespace):
    return ns.model(
        "Expect login",
        {
            "email": fields.String(required=True),
            "password": fields.String(required=True),
        },
    )
