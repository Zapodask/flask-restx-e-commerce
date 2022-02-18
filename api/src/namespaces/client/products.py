from flask_restx import Namespace, Resource
from flask import request

from src.utils.isBase64 import isBase64

from src.models import Products, Images, db


products = Namespace("products", "Products namespace")


@products.route("/")
class Index(Resource):
    def get(self):
        response = Products.query.all()
        query_products = [res.format() for res in response]

        return query_products


@products.route("/<int:id>")
@products.param("id", "Product identifier")
@products.response(404, "Product not found")
class Id(Resource):
    def get(self, id):
        product = Products.query.filter_by(id=id).first()

        return product
