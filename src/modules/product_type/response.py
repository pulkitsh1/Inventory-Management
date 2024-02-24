from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Method, Nested, Integer

ma = Marshmallow()

class ProductTypeResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    name = String(required=True, dump_only=True)
    description = String(required=True, dump_only=True)