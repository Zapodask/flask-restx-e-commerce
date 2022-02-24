from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from src.models import User


def auth_verify(api):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except:
                return api.abort(401, "Invalid token")

            return fn(*args, **kwargs)

        return decorator

    return wrapper


def admin_verify(api):
    def wrapper(fn):
        @wraps(fn)
        @auth_verify(api)
        def decorator(*args, **kwargs):
            id = get_jwt_identity()

            user = User.query.filter_by(id=id).first()

            if user.role != "admin":
                return api.abort(401, "You do not have permission to access this page")

            return fn(*args, **kwargs)

        return decorator

    return wrapper
