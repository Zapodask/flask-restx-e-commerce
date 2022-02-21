from flask_restx import fields, Namespace


def paginate_model(ns: Namespace, model):
    return ns.model(
        "Paginated items",
        {
            "items": fields.List(fields.Nested(model)),
            "page": fields.Integer(),
            "pages": fields.Integer(),
            "per_page": fields.Integer(),
            "total_items": fields.Integer(),
        },
    )
