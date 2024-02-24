from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Method, Nested, Integer
from marshmallow import validate, validates_schema, ValidationError
from src.modules.inventory.models import Inventory

ma = Marshmallow()

class Product(ma.SQLAlchemyAutoSchema):
    product_name = String(required=True,validate=[validate.Length(min=3)], load_only=True)
    quantity = Integer(required=True, load_only=True)
    price = Integer(required=True, load_only=True)

    @validates_schema
    def validate_data(self, data, **kwargs):
        product_name = data.get('product_name')

        if Inventory.query.filter_by(product_name=product_name).count():
            raise ValidationError(f"Product: {product_name} already exists.")
        
class Update(ma.SQLAlchemyAutoSchema):
    # product_name = String(required=True,validate=[validate.Length(min=3)], load_only=True)
    quantity = Integer(required=True, load_only=True)

class Delete(ma.SQLAlchemyAutoSchema):
    # product_name = String(required=True,validate=[validate.Length(min=3)], load_only=True)
    status = String(required=True, load_only=True)
