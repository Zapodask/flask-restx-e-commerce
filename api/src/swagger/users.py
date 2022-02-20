from flask_restx import fields, Namespace


def userSwagger(ns: Namespace):
    return ns.model(
        "User",
        {
            "id": fields.Integer(),
            "name": fields.String(),
            "surname": fields.String(),
            "email": fields.String(),
        },
    )


def expectUserSwagger(ns: Namespace):
    return ns.clone(
        "Expect user",
        userSwagger(ns),
        {
            "password": fields.String(required=True),
        },
    )
