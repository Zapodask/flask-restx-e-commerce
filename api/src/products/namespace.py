from flask_restx import Namespace, Resource
from flask import request
from src.utils.isBase64 import isBase64

from src.models import Products, Images, db


products = Namespace("products", "Products namespace")


@products.route("/")
class Index(Resource):
    def get(self):
        response = Products.query.all()
        products = [res.format() for res in response]

        return products

    def post(self):
        req = request.get_json()

        product = Products(
            name=req["name"],
            description=req["description"],
            price=req["price"],
        )

        if req["images"] and isinstance(req["images"], list):
            for img in req["images"]:
                if isBase64(img["base64"]):
                    product.images.append(
                        Images(
                            name=img["name"],
                            base64=img["base64"],
                            product_id=product.id,
                        )
                    )
                else:
                    return f'{img["name"]} only accepts base64 format', 400

        elif not isinstance(req["images"], list) and type(req["images"]) != None:
            return "Images has to be a list", 400

        db.session.add(product)
        db.session.commit()

        return {"message": "Product created"}, 201


@products.route("/<int:id>")
@products.param("id", "Product identifier")
@products.response(404, "Product not found")
class Id(Resource):
    def get(self, id):
        product = Products.query.filter_by(id=id).first()

        return product

    def put(self, id):
        req = request.get_json()

        product = Products.query.filter_by(id=id).first()

        if req["name"]:
            product.name = req["name"]

        if req["description"]:
            product.description = req["description"]

        if req["price"]:
            product.price = req["price"]

        db.session.add(product)
        db.session.commit()

        return {"message": "Product updated"}

    def delete(self, id):
        product = Products.query.filter_by(id=id).first()

        db.session.delete(product)
        db.session.commit()

        return {"message": "Product deleted"}
