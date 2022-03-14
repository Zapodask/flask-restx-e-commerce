from flask_restx import abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from os import getenv

from src.utils.calcPortage import calc_portage


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    surname = db.Column(db.String(90), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    orders = db.relationship(
        "Order",
        backref="user",
        lazy="subquery",
    )

    addresses = db.relationship(
        "Address",
        backref="user",
        lazy="subquery",
    )

    def __init__(
        self,
        name: str,
        surname: str,
        email: str,
        password: str,
        role: str = "client",
    ):
        self.name = name
        self.surname = surname
        self.email = email
        self.hash_password(password)
        self.role = role

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "role": self.role,
        }

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        try:
            if check_password_hash(self.password, password):
                return True
        except:
            return False


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    weight = db.Column(
        db.Float,
        nullable=False,
    )
    length = db.Column(
        db.Float,
        nullable=False,
    )
    width = db.Column(
        db.Float,
        nullable=False,
    )
    height = db.Column(
        db.Float,
        nullable=False,
    )

    order_product = db.relationship(
        "OrderProduct",
        backref=db.backref("product", lazy="select"),
        lazy="select",
    )

    images = db.relationship(
        "Image",
        backref=db.backref("product", lazy="select"),
        cascade="all,delete",
        lazy="select",
    )

    def __init__(
        self,
        name: str,
        weight: float,
        length: float,
        width: float,
        height: float,
        description: str = None,
        price: float = None,
        stock: int = 0,
    ):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height

    def format(self):
        imgs = []

        for img in self.images:
            imgs.append(
                {
                    "name": img.name,
                    "base64": img.base64,
                }
            )

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "images": imgs,
        }


class Image(db.Model):
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    base64 = db.Column(db.String, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    def __init__(self, name: str, base64: str, product_id: int):
        self.name = name
        self.base64 = base64
        self.product_id = product_id


order_product_relationship = db.Table(
    "order_product_relationship",
    db.Column(
        "order_product_id",
        db.Integer,
        db.ForeignKey("order_product.id"),
        primary_key=True,
    ),
    db.Column(
        "order_id",
        db.Integer,
        db.ForeignKey("order.id"),
        primary_key=True,
    ),
)


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    total_value = db.Column(db.Float, nullable=False)
    total_portage = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))

    products = db.relationship(
        "OrderProduct",
        secondary=order_product_relationship,
        lazy="subquery",
        cascade="all,delete",
        backref=db.backref("order", lazy=True),
    )

    def __init__(self, user_id: int, address_id: int, products: list):
        self.user_id = user_id

        address = Address.query.filter_by(id=address_id, user_id=user_id).first_or_404(
            description=f"Address not found"
        )

        self.address_id = address_id

        total_value = 0
        total_portage = 0
        deadline = 0

        for product in products:
            order_product = OrderProduct(
                product["quantity"],
                product["product_id"],
                address["cep"].replace("-", ""),
            )

            total_value += order_product.subtotal
            total_portage += order_product.portage
            deadline += order_product.deadline

            self.products.append(order_product)

        for item in self.products:
            item.product.stock -= item.quantity

        self.total_value = total_value
        self.total_portage = total_portage
        self.deadline = deadline / len(products)
        self.total = total_value + total_portage

    def format(self):
        return {
            "id": self.id,
            "total_value": self.total_value,
            "total_portage": self.total_total,
            "deadline": self.deadline,
            "total": self.total,
            "user_id": self.user_id,
            "address": self.address.format(),
            "products": [i.format() for i in self.products],
        }


class OrderProduct(db.Model):
    __tablename__ = "order_product"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    portage = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.Integer, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    def __init__(self, quantity: int, product_id: int, to_cep: str):
        self.quantity = quantity

        product = Product.query.filter_by(id=product_id).first()

        if quantity <= 0:
            abort(
                400,
                f"The quantity of the product id {product_id} must be greater than 0",
            )

        if product.stock - quantity < 0:
            abort(400, f"Product id {product_id} has only {product.stock}")

        self.product = product

        portage = calc_portage(
            "04510",
            getenv("SHOP_CEP"),
            to_cep,
            product["weight"] * quantity,
            1,
            product["length"],
            product["height"] * quantity,
            product["width"],
        )

        self.portage = portage["valor"]
        self.deadline = portage["prazo_entrega"]

        self.subtotal = product.price * quantity

    def format(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "subtotal": self.subtotal,
            "portage": self.portage,
            "deadline": self.deadline,
            "product": self.product.format(),
        }


class Address(db.Model):
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(9), nullable=False)
    state = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    neighborhood = db.Column(db.String, nullable=False)
    street = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    complement = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    orders = db.relationship(
        "Order",
        backref="address",
        lazy="dynamic",
    )

    def __init__(
        self,
        user_id: str,
        cep: str,
        state: str,
        city: str,
        neighborhood: str,
        street: str,
        number: int,
        complement: str = None,
    ):
        self.user_id = user_id
        self.cep = cep
        self.state = state
        self.city = city
        self.neighborhood = neighborhood
        self.street = street
        self.number = number
        self.complement = complement

    def format(self):
        return {
            "id": self.id,
            "cep": self.cep,
            "state": self.state,
            "city": self.city,
            "neighborhood": self.neighborhood,
            "street": self.street,
            "number": self.number,
            "complement": self.complement,
        }
