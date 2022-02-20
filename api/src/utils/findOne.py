def findOne(api, model, id: int):
    item = model.query.filter_by(id=id).first()

    if item is None:
        return api.abort(
            400,
            f"{model.__tablename__.capitalize()[:-1]} not found",
        )

    return item
