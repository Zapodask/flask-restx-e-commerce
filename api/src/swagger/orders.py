from flask_restx import fields, Namespace

from .products import marshal_product_model
from .addresses import marshall_address_model


def order_model(ns: Namespace):
    return ns.model(
        "Order",
        {
            "id": fields.Integer(),
            "total": fields.Float(),
            "user_id": fields.Integer(),
            "address": fields.Nested(marshall_address_model(ns)),
            "products": fields.List(fields.Nested(order_product_model(ns))),
        },
    )


def order_product_model(ns: Namespace):
    return ns.model(
        "Order product",
        {
            "id": fields.Integer(),
            "quantity": fields.Integer(),
            "subtotal": fields.Float(),
            "product": fields.Nested(marshal_product_model(ns)),
        },
    )


def expect_order_model(ns: Namespace):
    return ns.model(
        "Expect order",
        {
            "address_id": fields.Integer(required=True),
            "products": fields.List(
                fields.Nested(expect_order_product_model(ns)), required=True
            ),
        },
    )


def expect_order_product_model(ns: Namespace):
    return ns.model(
        "Expect order product",
        {
            "product_id": fields.Integer(),
            "quantity": fields.Integer(),
        },
    )


def expect_admin_order_model(ns: Namespace):
    return ns.clone(
        "Expect admin order",
        marshal_product_model(ns),
        {
            "user_id": fields.Integer(required=True),
        },
    )
