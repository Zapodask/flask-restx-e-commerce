from flask_restx import Namespace, Resource
from flask import request

from src.models import Products

from src.utils.paginate import paginate


products = Namespace("products", "Products namespace")


@products.route("/")
class Index(Resource):
    def get(self):
        args = request.args
        page = args.get("page")
        per_page = args.get("per_page")

        return paginate(Products, page, per_page)


@products.route("/<int:id>")
@products.param("id", "Product identifier")
@products.response(404, "Product not found")
class Id(Resource):
    def get(self, id):
        product = Products.query.filter_by(id=id).first()

        return product
