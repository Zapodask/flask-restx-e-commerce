from flask_restx import abort


def findOne(model, id: int):
    item = model.query.filter_by(id=id).first_or_404(
        description=f"{model.__tablename__.capitalize()[:-1]} not found"
    )

    return item
