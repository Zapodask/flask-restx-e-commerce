from flask_restx import abort


def findOne(model, id: int):
    item = model.query.filter_by(id=id).first()

    if item is None:
        return abort(
            404,
            message=f"{model.__tablename__.capitalize()[:-1]} not found",
        )

    return item
