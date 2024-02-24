from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Method, Nested, Integer
from marshmallow import validate, validates_schema, ValidationError
from src.modules.inventory.models import Inventory

ma = Marshmallow()

class ProductResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    product_name = String(required=True, dump_only=True)
    quantity = Integer(required=True, dump_only=True)
    price = Integer(required=True, dump_only=True)
    product_type = String(required=True, dump_only=True)
