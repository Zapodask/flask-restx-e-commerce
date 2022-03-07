from flask_restx import fields, Namespace

from . import add_id_to_model


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


def marshall_address_model(ns: Namespace):
    return add_id_to_model(ns, address_model(ns))
