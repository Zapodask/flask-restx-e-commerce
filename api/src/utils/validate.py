def validate(req, fields):
    ret = {
        "y": [],
        "n": [],
    }

    for f in fields:
        if f in req:
            ret["y"].append(f)
        else:
            ret["n"].append(f)

    return ret
