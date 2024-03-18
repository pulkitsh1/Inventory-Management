from flask_marshmallow import Marshmallow
from marshmallow.fields import String

ma = Marshmallow()

class UpdateStatus(ma.SQLAlchemyAutoSchema):
    status = String(required=True, load_only=True)