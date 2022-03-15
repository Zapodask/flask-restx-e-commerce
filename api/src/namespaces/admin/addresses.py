from flask_restx import Namespace, Resource
from flask import request

from src.models import Address, db

from src.decorators.auth import admin_verify
from src.utils.paginate import paginate
from src.swagger.addresses import address_model, marshall_address_model
from src.swagger.paginate import paginate_model


addresses = Namespace("Admin addresses", "Admin addresses routes", path="/addresses")


model = marshall_address_model(addresses)

list_model = paginate_model(addresses, model)

expect_model = address_model(addresses)


@addresses.route("/")
class Index(Resource):
    @addresses.doc("List addresses")
    @addresses.marshal_list_with(list_model)
    @addresses.response(404, "No addresses were found")
    @admin_verify(addresses)
    def get(self):
        """Find all addresses"""
        args = request.args
        page = args.get("page")
        per_page = args.get("per_page")

        return paginate(Address.query, page, per_page)

    @addresses.doc("Create address")
    @addresses.expect(expect_model)
    @admin_verify(addresses)
    def post(self):
        """Create a new address"""
        req = request.get_json()

        address = Address(
            user_id=req.get("user_id"),
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
    @addresses.doc("Find one address")
    @addresses.marshal_with(model)
    @admin_verify(addresses)
    def get(self, id):
        """Find one address"""
        return Address.query.filter_by(id=id).first_or_404(
            description=f"Address not found"
        )

    @addresses.doc("Update address")
    @admin_verify(addresses)
    def put(self, id):
        """Update address"""
        req = request.get_json()

        address = Address.query.filter_by(id=id).first_or_404(
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

    @addresses.doc("Delete address")
    @admin_verify(addresses)
    def delete(self, id):
        """Delete address"""
        address = Address.query.filter_by(id=id).first_or_404(
            description=f"Address not found"
        )

        db.session.delete(address)
        db.session.commit()

        return {"message": "Address deleted"}
