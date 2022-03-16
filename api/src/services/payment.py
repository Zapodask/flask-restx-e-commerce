import mercadopago

from src.models import Order

sdk = mercadopago.SDK("MP_ACCESS_TOKEN")


def create_payment(order: Order, payment_method: str):
    """Create payment

    Args:
        order (Order): Order model
        payment_method (str): "pix" or "bolbradesco"

    Returns:
        dict: pix key or ticket
    """
    user = order.user
    address = order.address

    cpf = user.cpf

    payment_data = {
        "transaction_amount": order.total,
        "description": "",
        "payment_method_id": payment_method,
        "payer": {
            "email": user.email,
            "first_name": user.name,
            "last_name": user.surname,
            "identification": {"type": "CPF", "number": cpf[:9] + "-" + cpf[9:]},
            "address": {
                "zip_code": address.cep,
                "street_name": address.street,
                "street_number": address.number,
                "neighborhood": address.neighborhood,
                "city": address.city,
                "federal_unit": address.state,
            },
        },
    }

    payment_response = sdk.payment().create(payment_data)
    return payment_response["response"]
