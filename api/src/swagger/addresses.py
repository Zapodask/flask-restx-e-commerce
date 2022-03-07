from flask_restx import fields, Namespace


def address_model(ns: Namespace):
    return ns.model(
        "Address",
        {
            "id": fields.Integer(),
            "cep": fields.String(),
            "state": fields.String(),
            "city": fields.String(),
            "neighborhood": fields.String(),
            "street": fields.String(),
            "number": fields.Integer(),
            "complement": fields.String(),
        },
    )
