from flask_restx import fields, Namespace


def product_model(ns: Namespace):
    return ns.model(
        "Product",
        {
            "id": fields.Integer(),
            "name": fields.String(),
            "description": fields.String(),
            "price": fields.Float(),
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
