from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Method, Nested, Integer
from marshmallow import validate, validates_schema, ValidationError
from src.modules.inventory.models import Inventory

ma = Marshmallow()

class Update(ma.SQLAlchemyAutoSchema):
    status = String(required=True, load_only=True)