from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Method, Nested, Integer
from marshmallow import validate, validates_schema, ValidationError
from src.modules.user.models import User

ma = Marshmallow()

class EmpAddchema(ma.SQLAlchemyAutoSchema):
    name = String(required=False,validate=[validate.Length(min=3)], load_only=True)
    email = String(required=True,validate=[validate.Email()], load_only=True)
    employee_id = Integer(required=False, load_only=True)

    @validates_schema
    def validate_data(self, data, **kwargs):
        email = data.get('email')

        if User.query.filter_by(email=email).count():
            raise ValidationError(f"Email {email} already exists.")