from flask_restx import fields, Namespace

from . import add_id_to_model


def user_model(ns: Namespace):
    return ns.model(
        "User",
        {
            "name": fields.String(required=True),
            "surname": fields.String(required=True),
            "email": fields.String(required=True),
            "role": fields.String(required=True),
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


def marshal_user_model(ns: Namespace):
    return add_id_to_model(ns, user_model(ns))
