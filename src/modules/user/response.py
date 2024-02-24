from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Method, Nested, Integer
from marshmallow import validate, validates_schema, ValidationError
from src.modules.inventory.models import Inventory

ma = Marshmallow()

class UserResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    name = String(required=True, dump_only=True)
    email = String(required=True, dump_only=True)

class UserRolesResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    name = String(required=True, dump_only=True)
    user_id = Integer(required=True, dump_only=True)
    product_type_id = Integer(required=True, dump_only=True)