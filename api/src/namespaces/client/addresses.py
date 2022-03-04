from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import get_jwt_identity

from src.models import Address, db

from src.decorators.auth import auth_verify
from src.utils.paginate import paginate


addresses = Namespace("Addresses", "Addresses routes", path="/addresses")


@addresses.route("/")
class Index(Resource):
    @auth_verify(addresses)
    def get(self):
        """Find all user addresses"""
        args = request.args
        page = args.get("page")
        per_page = args.get("per_page")

        user_id = get_jwt_identity()

        return paginate(Address.query.filter_by(user_id=user_id), page, per_page)

    @auth_verify(addresses)
    def post(self):
        user_id = get_jwt_identity()

        req = request.get_json()

        address = Address(
            user_id=user_id,
            cep=req.get("cep"),
            state=req.get("state"),
            city=req.get("city"),
            neighborhood=req.get("neighborhood"),
            street=req.get("street"),
            number=req.get("number"),
            complement=req.get("complement"),
        )

        db.session.add(address)
        db.session.commit()

        return {"message": "Address created"}, 201


@addresses.route("/<int:id>")
@addresses.param("id", "Address identifier")
@addresses.response(404, "Address not found")
class Id(Resource):
    def get(self, id):
        user_id = get_jwt_identity()

        return Address.query.filter_by(id=id, user_id=user_id).first_or_404(
            description=f"Address not found"
        )

    def put(self, id):
        user_id = get_jwt_identity()

        req = request.get_json()

        address = Address.query.filter_by(id=id, user_id=user_id).first_or_404(
            description=f"Address not found"
        )

        if req.get("cep"):
            address.cep = req.get("cep")

        if req.get("state"):
            address.state = req.get("state")

        if req.get("city"):
            address.city = req.get("city")

        if req.get("neighborhood"):
            address.neighborhood = req.get("neighborhood")

        if req.get("street"):
            address.street = req.get("street")

        if req.get("number"):
            address.number = req.get("number")

        if req.get("complement"):
            address.complement = req.get("complement")

        db.session.add(address)
        db.session.commit()

        return {"message": "Address updated"}

    def delete(self, id):
        user_id = get_jwt_identity()

        address = Address.query.filter_by(id=id, user_id=user_id).first_or_404(
            description=f"Address not found"
        )

        db.session.delete(address)
        db.session.commit()

        return {"message": "Address deleted"}
