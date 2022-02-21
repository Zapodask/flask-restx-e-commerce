from flask_restx import Namespace, Resource, fields
from flask import request

from src.models import Products

from src.utils.paginate import paginate
from src.utils.findOne import findOne

from src.swagger.products import product_model
from src.swagger.paginate import paginate_model


products = Namespace("Products", "Products routes", path="/products")


model = product_model(products)

list_model = paginate_model(products, model)


@products.route("/")
class Index(Resource):
    @products.doc("Client products")
    @products.response(400, "Products not found")
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
