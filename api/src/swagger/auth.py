from flask_restx import fields, Namespace


def expect_login_model(ns: Namespace):
    return ns.model(
        "Expect login",
        {
            "email": fields.String(required=True),
            "password": fields.String(required=True),
        },
    )


def expect_register_model(ns: Namespace):
    return ns.clone(
        "Expect register",
        expect_login_model(ns),
        {
            "name": fields.String(required=True),
            "surname": fields.String(required=True),
        },
    )
