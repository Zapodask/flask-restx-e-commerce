from flask_restx import Namespace, Resource, fields
from flask import request

from src.models import Products

from src.utils.paginate import paginate
from src.utils.findOne import findOne

from src.swagger.products import productSwagger
from src.swagger.paginate import paginateSwagger


products = Namespace("products", "Products namespace")


model = productSwagger(products)

list_model = paginateSwagger(products, model)


@products.route("/")
class Index(Resource):
    @products.doc(responses={400: {"Produtos não encontrados"}})
    @products.marshal_list_with(list_model)
    def get(self):
        args = request.args
        page = args.get("page")
        per_page = args.get("per_page")

        return paginate(products, Products, page, per_page)


@products.route("/<int:id>")
@products.param("id", "Product identifier")
@products.response(400, "Product not found")
class Id(Resource):
    @products.doc()
    def get(self, id):
        product = findOne(products, Products, id)

        return product.format()
