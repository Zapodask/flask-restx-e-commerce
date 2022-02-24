from flask_restx import Namespace, Resource
from flask import request

from src.models import Order, db

from src.utils.paginate import paginate
from src.utils.findOne import findOne


orders = Namespace("Admin orders", "Admin orders routes")


@orders.route("/")
class Index(Resource):
    def get(self):
        args = request.args
        page = args.get("page")
        per_page = args.get("per_page")

        return paginate(Order, page, per_page)

    def post(self):
        req = request.get_json()

        order = Order(
            user_id=req.get("user_id"),
            products=req.get("products"),
        )

        db.session.add(order)
        db.session.commit()

        return


@orders.route("/<int:id>")
@orders.param("id", "Order identifier")
@orders.response(404, "Order not found")
class Index(Resource):
    def get(self, id):
        res = findOne(Order, id)

        return res.format()

    def put(self, id):
        return

    def delete(self, id):
        order = findOne(Order, id)

        db.session.delete(order)
        db.session.commit()

        return
