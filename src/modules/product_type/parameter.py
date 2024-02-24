from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Method, Nested, Integer
from marshmallow import validate, validates_schema, ValidationError
from src.modules.product_type.models import Product_type

ma = Marshmallow()

class ProductType_Schema(ma.SQLAlchemyAutoSchema):
    name = String(required=False, load_only=True)
    description = String(required=True,validate=[validate.Length(min=3)], load_only=True)

    @validates_schema
    def validate_data(self, data, **kwargs):
        name = data.get('name')

        if Product_type.query.filter_by(name=name).count():
            raise ValidationError(f"Product Type: {name} already exists.")
        
class ProductTypeDelete(ma.SQLAlchemyAutoSchema):
    status = String(required=True, load_only=True)

class ProductTypeUpdate(ma.SQLAlchemyAutoSchema):
    name = String(required=True, load_only=True)
    description = String(required=True, load_only=True)