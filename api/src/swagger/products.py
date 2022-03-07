from flask_restx import fields, Namespace

from . import add_id_to_model


def product_model(ns: Namespace):
    return ns.model(
        "Product",
        {
            "name": fields.String(required=True),
            "description": fields.String(),
            "price": fields.Float(),
            "stock": fields.Integer(),
            "images": fields.List(fields.Nested(image_model(ns))),
        },
    )


def image_model(ns: Namespace):
    return ns.model(
        "Image",
        {
            "name": fields.String(),
            "base64": fields.String(),
        },
    )


def marshal_product_model(ns: Namespace):
    return add_id_to_model(ns, product_model(ns))
