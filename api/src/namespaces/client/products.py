from flask_restx import Namespace, Resource, fields
from flask import request

from src.models import Product

from src.utils.paginate import paginate
from src.utils.findOne import findOne

from src.swagger.products import marshal_product_model
from src.swagger.paginate import paginate_model


products = Namespace("Products", "Products routes", path="/products")


model = marshal_product_model(products)

list_model = paginate_model(products, model)


@products.route("/")
class Index(Resource):
    @products.doc("List products")
    @products.response(404, "Products not found")
    @products.marshal_list_with(list_model)
    def get(self):
        args = request.args
        page = args.get("page")
        per_page = args.get("per_page")

        return paginate(Product.query, page, per_page)


@products.route("/<int:id>")
@products.param("id", "Product identifier")
class Id(Resource):
    @products.doc("Get product")
    @products.response(404, "Product not found")
    def get(self, id):
        product = findOne(Product, id)

        return product.format()
