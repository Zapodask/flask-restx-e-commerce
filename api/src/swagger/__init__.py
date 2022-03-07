from flask_restx import fields, Namespace


def add_id_to_model(ns: Namespace, model):
    return ns.clone(
        "Add id, to model",
        model,
        {
            "id": fields.Integer(),
        },
    )
