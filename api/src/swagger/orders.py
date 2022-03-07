from flask_restx import fields, Namespace

from .products import product_model
from .addresses import address_model


def order_model(ns: Namespace):
    return ns.model(
        "Order",
        {
            "id": fields.Integer(),
            "total": fields.Float(),
            "user_id": fields.Integer(),
            "address": fields.Nested(address_model(ns)),
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
            "product": fields.Nested(product_model(ns)),
        },
    )


def expect_order_model(ns: Namespace):
    return ns.model(
        "Expect order",
        {
            "user_id": fields.Integer(),
            "address_id": fields.Integer(),
            "products": fields.List(fields.Nested(expect_order_products_model(ns))),
        },
    )


def expect_order_products_model(ns: Namespace):
    return ns.model(
        "Expect order",
        {
            "id": fields.Integer(),
            "quantity": fields.Integer(),
        },
    )


def expect_order_client_model(ns: Namespace):
    return ns.model(
        "Expect order client",
        {
            "address_id": fields.Integer(),
            "products": fields.List(fields.Nested(expect_order_products_model(ns))),
        },
    )
