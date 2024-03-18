from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer,Boolean

ma = Marshmallow()

class EmployeeResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    name = String(required=True, dump_only=True)
    email = String(required=True, dump_only=True)
    employee_id = Integer(required=True, dump_only=True)
    status = Boolean(required=True, dump_only=True)