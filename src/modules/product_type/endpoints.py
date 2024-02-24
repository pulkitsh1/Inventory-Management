from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_
from src.modules.product_type.models import Product_type
from src.service_modules.auth import is_super_admin
from src.service_modules.db.conn import db
from src.modules.product_type.parameter import ProductType_Schema, ProductTypeDelete, ProductTypeUpdate
from src.modules.product_type.response import ProductTypeResponse

blp = Blueprint('productype',__name__)

class ProductTypeOperations(MethodView):

    @blp.response(HTTPStatus.OK,schema=ProductTypeResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self,id):
        try:
            if id == 'all':
                res = Product_type.query.all()
            else:
                res = Product_type.query.filter_by(id=id).all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}

    @blp.arguments(schema=ProductType_Schema())
    @jwt_required()
    @is_super_admin    
    def post(self, req_data,id):
        try:
            name = req_data.get('name').lower()
            entry = Product_type(name=name, description=req_data.get('description'),status='active')
            db.session.add(entry)
            db.session.commit()

            return {'message':'Product Type sucessfully added',"status": HTTPStatus.OK}
        except Exception as e:
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
    @blp.arguments(schema=ProductTypeUpdate())
    @jwt_required()
    @is_super_admin    
    def put(self, req_data, id):
        try:
            res = Product_type.query.filter_by(id=id).first()
            res.description = req_data.get('description')
            db.session.commit()

            return {'message':'Product Type description sucessfully updated',"status": HTTPStatus.OK}
        except Exception as e:
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
    @blp.arguments(schema=ProductTypeDelete())
    @jwt_required()
    @is_super_admin
    def delete(self, req_data, id):
        try:
            res = Product_type.query.filter_by(id=id).first()
            res.status = req_data.get('status').lower()

            for r in res.product:
                r.status = req_data.get('status').lower()
            db.session.commit()

            return {'message':'Product Type sucessfully deleted',"status": HTTPStatus.OK}
        except Exception as e:
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
blp.add_url_rule('/product/type/<id>', view_func=ProductTypeOperations.as_view('product_type_operation'))
