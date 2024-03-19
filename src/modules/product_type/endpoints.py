from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from src.modules.product_type.models import Product_type
from src.service_modules.auth import is_super_admin
from src.service_modules.db.conn import db
from src.modules.product_type.parameter import ProductType_Schema, ProductTypeDelete, ProductTypeUpdate
from src.modules.product_type.response import ProductTypeResponse

api = Blueprint("productype",__name__,description="Operations on Product Type")

@api.route('/product_type/')
class ProductType(MethodView):

    @api.response(HTTPStatus.OK,schema=ProductTypeResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self):
        try:
            res = Product_type.query.all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
    @api.arguments(schema=ProductType_Schema())
    @jwt_required()
    @is_super_admin    
    def post(self, req_data):
        try:
            name = req_data.get('name').lower()
            entry = Product_type(name=name, description=req_data.get('description'),status='active')
            db.session.add(entry)
            db.session.commit()

            return {'message':'Product Type sucessfully added',"status": HTTPStatus.OK}
        except Exception as e:
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}

@api.route('/product_type/<id>')
class ProductTypeOperations(MethodView):

    @api.response(HTTPStatus.OK,schema=ProductTypeResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self,id):
        try:
            res = Product_type.query.filter_by(id=id).all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}

        
    @api.arguments(schema=ProductTypeUpdate())
    @jwt_required()
    @is_super_admin    
    def put(self, req_data, id):
        try:
            res = Product_type.query.filter_by(id=id).first()
            if res == None:
                raise Exception("The id given doesn't exist.", HTTPStatus.NOT_FOUND)
            res.description = req_data.get('description')
            db.session.commit()

            return {'message':'Product Type description sucessfully updated',"status": HTTPStatus.OK}
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            return {'error': error_message, 'status': status_code}
        
    @api.arguments(schema=ProductTypeDelete())
    @jwt_required()
    @is_super_admin
    def delete(self, req_data, id):
        try:
            res = Product_type.query.filter_by(id=id).first()
            if res == None:
                raise Exception("The id given doesn't exist.",HTTPStatus.NOT_FOUND)
            res.status = req_data.get('status').lower()

            for r in res.product:
                r.status = req_data.get('status').lower()
            db.session.commit()

            return {'message':'Product Type sucessfully deleted',"status": HTTPStatus.OK}
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            return {'error': error_message, 'status': status_code}
        
@api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}
