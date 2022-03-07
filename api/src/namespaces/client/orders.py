from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import get_jwt_identity

from src.models import Order, db

from src.utils.paginate import paginate
from src.decorators.auth import auth_verify
from src.swagger.orders import order_model, expect_order_client_model
from src.swagger.paginate import paginate_model


orders = Namespace("Orders", "Orders routes", path="/orders")


model = order_model(orders)

list_model = paginate_model(orders, model)

expect_order = expect_order_client_model(orders)


@orders.route("/")
class Index(Resource):
    @orders.doc("List ordes")
    @orders.marshal_list_with(list_model)
    @orders.response(404, "No orders were found")
    @auth_verify(orders)
    def get(self):
        """Find client orders"""
        args = request.args
        page = args.get("page")
        per_page = args.get("per_page")

        user_id = get_jwt_identity()

        return paginate(Order.query.filter_by(user_id=user_id), page, per_page)

    @orders.doc("Create order")
    @orders.expect(expect_order)
    @auth_verify(orders)
    def post(self):
        """Create client order"""
        req = request.get_json()

        user_id = get_jwt_identity()

        order = Order(
            user_id=user_id,
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
    @auth_verify(orders)
    def get(self, id: int):
        """Find client order"""
        user_id = get_jwt_identity()

        order = Order.query.filter_by(id=id, user_id=user_id).first_or_404(
            description=f"Order not found"
        )

        return order.format()
