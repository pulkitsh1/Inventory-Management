from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer

ma = Marshmallow()

class ProductResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    product_name = String(required=True, dump_only=True)
    quantity = Integer(required=True, dump_only=True)
    price = Integer(required=True, dump_only=True)
    product_type_id = Integer(required=True, dump_only=True)
