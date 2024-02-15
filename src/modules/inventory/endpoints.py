from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from src.service_modules.db.conn import db
from src.modules.inventory.models import Inventory
from src.modules.user.models import User
from src.modules.inventory.parameter import Product, Update, Delete, ProductTypeDelete
from src.modules.inventory.response import ProductResponse, ProductTypeResponse

blp = Blueprint('inventory',__name__)

class Inventory_Operations(MethodView):

    @blp.response(HTTPStatus.OK,schema=ProductResponse(many=True))
    @jwt_required()
    def get(self):
        try:
            email = get_jwt()['sub']
            email_exist = User.query.filter_by(email=email).first()
            type = email_exist.product_type

            res = Inventory.query.filter_by(product_type=type).all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}

    @blp.arguments(schema=Product())
    @jwt_required()
    def post(self, req_data):
        try:
            email = get_jwt()['sub']
            email_exist = User.query.filter_by(email=email).first()
            type = email_exist.product_type
            product_name = req_data.get('product_name').lower()
            entry = Inventory(product_name=product_name, price=req_data.get('price'), quantity=req_data.get('quantity'), product_type=type)
            db.session.add(entry)
            db.session.commit()
            return {"message":"Product added successfully.","status": HTTPStatus.OK}
        except Exception as e:
            return {"error":f"{str(e)}","status": HTTPStatus.INTERNAL_SERVER_ERROR}
    
    @blp.arguments(schema=Update())
    @jwt_required()
    def put(self, get_data):
        try:
            product_data = Inventory.query.filter_by(product_name=get_data.get('product_name')).first()
            
            product_data.quantity = product_data.quantity + get_data.get('quantity')
            db.session.commit()

            return {"message":"Quanity of the product successfully updated.","status": HTTPStatus.OK}
        except Exception as e:
            return {'error':f'{str(e)}','status':HTTPStatus.INTERNAL_SERVER_ERROR}
        
    @blp.arguments(schema=Delete())
    @jwt_required()
    def delete(self, get_data):
        try:
            res = Inventory.query.filter_by(product_name=get_data.get('product_name')).first()
            
            db.session.delete(res)
            db.session.commit()

            return {'message':'Product sucessfully deleted',"status": HTTPStatus.OK}
        except Exception as e:
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}

blp.add_url_rule('/inventory', view_func=Inventory_Operations.as_view('Inventory_Operation'))

class ProductTypeOperations(MethodView):

    @blp.response(HTTPStatus.OK,schema=ProductTypeResponse(many=True))
    @jwt_required()
    def get(self):
        try:
            # email = get_jwt()['sub']
            # email_exist = User.query.filter_by(email=email).first()
            # type = email_exist.product_type

            res = User.query.all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
    @blp.arguments(schema=ProductTypeDelete())
    @jwt_required()
    def delete(self, req_data):
        try:
            res = Inventory.query.filter_by(product_type=req_data.get('product_type')).all()
            prod = User.query.filter_by(product_type=req_data.get('product_type')).first()
            
            prod.product_type = 'null'
            
            for r in res:
                db.session.delete(r)
            db.session.commit()

            return {'message':'Product Type sucessfully deleted',"status": HTTPStatus.OK}
        except Exception as e:
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
blp.add_url_rule('/product/type', view_func=ProductTypeOperations.as_view('product_type_operation'))

@blp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}