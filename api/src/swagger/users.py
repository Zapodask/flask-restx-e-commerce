from flask_restx import fields, Namespace


def user_model(ns: Namespace):
    return ns.model(
        "User",
        {
            "id": fields.Integer(),
            "name": fields.String(),
            "surname": fields.String(),
            "email": fields.String(),
        },
    )


def expect_user_model(ns: Namespace):
    return ns.clone(
        "Expect user",
        user_model(ns),
        {
            "password": fields.String(required=True),
        },
    )
