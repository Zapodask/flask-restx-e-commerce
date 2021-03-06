from flask_restx import Namespace, Resource
from flask import request

from src.models import Product, Image, db

from src.decorators.auth import admin_verify
from src.utils.isBase64 import isBase64
from src.utils.paginate import paginate
from src.swagger.paginate import paginate_model
from src.swagger.products import marshal_product_model


products = Namespace("Admin products", "Admin products routes")


model = marshal_product_model(products)

list_model = paginate_model(products, model)


@products.route("/")
class Index(Resource):
    @products.doc("List products")
    @products.response(404, "Products not found")
    @products.marshal_list_with(list_model)
    @admin_verify(products)
    def get(self):
        args = request.args
        page = args.get("page")
        per_page = args.get("per_page")

        return paginate(Product.query, page, per_page)

    @products.doc("Create product")
    @products.expect(model)
    @admin_verify(products)
    def post(self):
        req = request.get_json()

        product = Product(
            name=req.get("name"),
            description=req.get("description"),
            price=req.get("price"),
            stock=req.get("stock"),
            weight=req.get("weight"),
            length=req.get("length"),
            width=req.get("width"),
            height=req.get("height"),
        )

        if req["images"] and isinstance(req["images"], list):
            for img in req["images"]:
                if isBase64(img["base64"]):
                    product.images.append(
                        Image(
                            name=img["name"],
                            base64=img["base64"],
                            product_id=product.id,
                        )
                    )
                else:
                    return {"message": f'{img["name"]} only accepts base64 format'}, 400

        elif not isinstance(req["images"], list) and type(req["images"]) != None:
            return "Images has to be a list", 400

        db.session.add(product)
        db.session.commit()

        return {"message": "Product created"}, 201


@products.route("/<int:id>")
@products.param("id", "Product identifier")
@products.response(404, "Product not found")
class Id(Resource):
    @products.doc("Find product")
    @products.marshal_with(model)
    @admin_verify(products)
    def get(self, id: int):
        product = Product.query.filter_by(id=id).first()

        return product.format()

    @products.doc("Update product")
    @admin_verify(products)
    def put(self, id: int):
        req = request.get_json()

        product = Product.query.filter_by(id=id).first()

        if req.get("name"):
            product.name = req["name"]

        if req.get("description"):
            product.description = req["description"]

        if req.get("price"):
            product.price = req["price"]

        db.session.add(product)
        db.session.commit()

        return {"message": "Product updated"}

    @products.doc("Delete product")
    @admin_verify(products)
    def delete(self, id: int):
        product = Product.query.filter_by(id=id).first()

        db.session.delete(product)
        db.session.commit()

        return {"message": "Product deleted"}
