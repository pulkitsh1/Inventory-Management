from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer, Raw
from marshmallow import validate

ma = Marshmallow()

class TransactionSchema(ma.SQLAlchemyAutoSchema):
    product_name = String(required=True,validate=[validate.Length(min=3)], load_only=True)
    quantity = Integer(required=True, load_only=True)
    price_per_unit = Integer(required=False, load_only=True)
    total_price = Integer(required=True, load_only=True)
    transaction_id = Integer(required=True, load_only=True)
    product_type = String(required=False, load_only=True)
    attachments = Raw(type='file',required=False, load_only=True)

class TransactionIDSchema(ma.SQLAlchemyAutoSchema):
    transaction_id = Integer(required=True, load_only=True)