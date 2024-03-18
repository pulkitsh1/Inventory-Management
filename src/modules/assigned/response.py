from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer,Date

ma = Marshmallow()

class AssignedResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    product_id = Integer(required=True, dump_only=True)
    quantity = Integer(required=True, dump_only=True)
    employee_id = Integer(required=True, dump_only=True)
    product_type_id = Integer(required=True, dump_only=True)
    assignment_date = Date(required=True, dump_only=True)
    return_date = Date(required=True, dump_only=True)
    unique_code = String(required=True, dump_only=True)
    status = String(required=True, dump_only=True)