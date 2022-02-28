from flask_restx import abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


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
        lazy="dynamic",
    )

    adresses = db.relationship(
        "Address",
        backref="user",
        lazy="dynamic",
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
        description: str = None,
        price: float = None,
        stock: int = 0,
    ):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

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
    total = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))

    products = db.relationship(
        "OrderProduct",
        secondary=order_product_relationship,
        lazy="subquery",
        cascade="all,delete",
        backref=db.backref("order", lazy=True),
    )

    def __init__(self, user_id: int, products: list):
        self.user_id = user_id

        total = 0

        for product in products:
            order_product = OrderProduct(product["quantity"], product["id"])

            total += order_product.subtotal

            self.products.append(order_product)

        for item in self.products:
            item.product.stock -= item.quantity

        self.total = total

    def format(self):
        return {
            "id": self.id,
            "total": self.total,
            "user_id": self.user_id,
            "products": [i.format() for i in self.products],
        }


class OrderProduct(db.Model):
    __tablename__ = "order_product"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    subtotal = db.Column(db.Float)

    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    def __init__(self, quantity: int, product_id: int):
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

        self.subtotal = product.price * quantity

    def format(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "subtotal": self.subtotal,
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
        cep: str,
        state: str,
        city: str,
        neighborhood: str,
        street: str,
        number: int,
        complement: str = None,
    ):
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
