from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Method, Nested, Integer,Date
from src.modules.inventory.models import Inventory

ma = Marshmallow()

class AssignedResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    product_id = Integer(required=True, dump_only=True)
    quantity = Integer(required=True, dump_only=True)
    employee_id = Integer(required=True, dump_only=True)
    product_type_id = Integer(required=True, dump_only=True)
    assignment_date = Date(required=True, dump_only=True)
    status = String(required=True, dump_only=True)