from flask_restx import Namespace, Resource
from flask import request

from src.models import Order, db

from src.utils.paginate import paginate
from src.utils.findOne import findOne
from src.decorators.auth import admin_verify
from src.swagger.orders import order_model, expect_admin_order_model
from src.swagger.paginate import paginate_model


orders = Namespace("Admin orders", "Admin orders routes")


model = order_model(orders)

list_model = paginate_model(orders, model)

expect_order = expect_admin_order_model(orders)


@orders.route("/")
class Index(Resource):
    @orders.doc("List ordes")
    @orders.marshal_list_with(list_model)
    @orders.response(404, "No orders were found")
    @admin_verify(orders)
    def get(self):
        args = request.args
        page = args.get("page")
        per_page = args.get("per_page")

        return paginate(Order.query, page, per_page)

    @orders.doc("Create order")
    @orders.expect(expect_order)
    @admin_verify(orders)
    def post(self):
        req = request.get_json()

        order = Order(
            user_id=req.get("user_id"),
            address_id=req.get("address_id"),
            products=req.get("products"),
        )

        db.session.add(order)
        db.session.commit()

        return {"message": "Order created"}, 201


@orders.route("/<int:id>")
@orders.param("id", "Order identifier")
@orders.response(404, "Order not found")
class Index(Resource):
    @orders.doc("Find order")
    @orders.marshal_with(model)
    @admin_verify(orders)
    def get(self, id: int):
        order = findOne(Order, id)

        return order.format()

    @orders.doc("Delete order")
    @admin_verify(orders)
    def delete(self, id: int):
        order = findOne(Order, id)

        db.session.delete(order)
        db.session.commit()

        return {"message": "Order deleted"}, 200
