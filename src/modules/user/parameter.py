from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Method, Nested, Integer
from marshmallow import validate, validates_schema, ValidationError
from src.modules.user.models import User

ma = Marshmallow()

class SignupSchema(ma.SQLAlchemyAutoSchema):
    name = String(required=True,validate=[validate.Length(min=3)], load_only=True)
    email = String(required=True,validate=[validate.Email()], load_only=True)
    password = String(required=True)
    confirm_password = String(required=True)

    @validates_schema
    def validate_data(self, data, **kwargs):
        email = data.get('email')

        if User.query.filter_by(email=email).count():
            raise ValidationError(f"Email {email} already exists.")
        
class LoginSchema(ma.SQLAlchemyAutoSchema):
    email = String(required=True,validate=[validate.Email()], load_only=True)
    password = String(required=True, load_only=True)

class ChangePasswordSchema(ma.SQLAlchemyAutoSchema):
    password = String(required=True)
    new_password = String(required=True)
    confirm_password = String(required=True)

class UpdateSchema(ma.SQLAlchemyAutoSchema):
    name = String(required=True, load_only=True)
    product_type = String(required=True, load_only=True)

class DeleteUserSchema(ma.SQLAlchemyAutoSchema):
    name = String(required=True, load_only=True)

class RoleAddSchema(ma.SQLAlchemyAutoSchema):
    name = String(required=True, load_only=True)
    user_id = Integer(required=True, load_only=True)
    product_id = Integer(required=True, load_only=True)

class RoleUpdateSchema(ma.SQLAlchemyAutoSchema):
    user_id = Integer(required=True, load_only=True)
    # role_id = Integer(required=True, load_only=True)