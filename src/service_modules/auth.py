from functools import wraps
from flask_jwt_extended import get_jwt
from http import HTTPStatus

def is_super_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = get_jwt()['sub']
        if res[1] not in ['super_admin']:
            return {"error": "This endpoint is restricted to super admin only!", "status": HTTPStatus.UNAUTHORIZED}
        return func(*args, **kwargs)
    return wrapper

def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = get_jwt()['sub']
        if res[1] not in ['admin','super_admin']:
            return {"error": "This endpoint is restricted to admin and super admin only!", "status": HTTPStatus.UNAUTHORIZED}
        return func(*args, **kwargs)
    return wrapper

def is_member(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = get_jwt()['sub']
        if res[1] not in ['member','admin','super_admin']:
            return {"error": "This endpoint is restricted to member, admin and super admin only!", "status": HTTPStatus.UNAUTHORIZED}
        return func(*args, **kwargs)
    return wrapper

def is_reader(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = get_jwt()['sub']
        if res[1] not in ['reader','member','admin','super_admin']:
            return {"error": "You need to get a role assigned by super admin", "status": HTTPStatus.UNAUTHORIZED}
        return func(*args, **kwargs)
    return wrapper
