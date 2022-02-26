from flask_restx import abort


def paginate(query, page: str = None, per_page: str = None):
    page = page or 1
    per_page = per_page or 10

    response = query.paginate(int(page), int(per_page))

    if response.items == []:
        return abort(404, "No items were found")

    items = [res.format() for res in response.items]

    ret = {
        "items": items,
        "page": page,
        "pages": response.pages,
        "per_page": per_page,
        "total_items": response.total,
    }

    return ret
