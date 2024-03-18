from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer, Date

ma = Marshmallow()

class TransactionResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    product_name = String(required=True, dump_only=True)
    price_per_unit = Integer(required=True, dump_only=True)
    total_price = Integer(required=True, dump_only=True)
    quantity = Integer(required=True, dump_only=True)
    product_type = String(required=True, dump_only=True)
    order_placement_date = Date(required=True, dump_only=True)
    transaction_id = Integer(required=True, dump_only=True)
    attachments = String(required=True, dump_only=True)
    order_status = String(required=True, dump_only=True)