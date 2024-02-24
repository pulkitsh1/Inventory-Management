from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_
from src.service_modules.db.conn import db
from src.modules.inventory.models import Inventory
from src.modules.product_type.models import Product_type
from src.modules.inventory.parameter import Product, Update, Delete
from src.modules.inventory.response import ProductResponse
from src.service_modules.auth import is_admin,is_member,is_reader,is_super_admin

blp = Blueprint('inventory',__name__)

class Inventory_Operations(MethodView):

    @blp.response(HTTPStatus.OK,schema=ProductResponse(many=True))
    @jwt_required()
    @is_reader
    def get(self,type,id):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                if id == 'all':
                    res= Product_type.query.filter_by(name=type).first()
                    res = Inventory.query.filter_by(product_type_id=res.id).all()
                else:
                    res = Inventory.query.filter_by(id=id).all()
                    if res[0].products.name != type:
                            res = []
            else:
                domain = domain[2]

                if type in domain:
                    if id == 'all':
                        res= Product_type.query.filter_by(name=type).first()
                        res = Inventory.query.filter_by(product_type_id=res.id).all()
                    else:
                        res = Inventory.query.filter(
                            and_(
                                Inventory.id == id,
                                Inventory.status == 'active'
                            )).all()
                        if res[0].products.name != type:
                            res = []
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}

    @blp.arguments(schema=Product())
    @jwt_required()
    @is_admin
    def post(self, req_data,type,id):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                res = Product_type.query.filter_by(name=type).first()
                product_name = req_data.get('product_name').lower()
                entry = Inventory(product_name=product_name, price=req_data.get('price'), quantity=req_data.get('quantity'), products=res, status = "active")
                db.session.add(entry)
                db.session.commit()
                return {"message":"Product added successfully.","status": HTTPStatus.OK}
            else:
                domain = domain[2]

                if type in domain:
                    res = Product_type.query.filter_by(name=type).first()
                    product_name = req_data.get('product_name').lower()
                    entry = Inventory(product_name=product_name, price=req_data.get('price'), quantity=req_data.get('quantity'), products=res, status = "active")
                    db.session.add(entry)
                    db.session.commit()
                    return {"message":"Product added successfully.","status": HTTPStatus.OK}
                else:
                    return {"error":"The product type you are trying to add is out of your domain",'status': HTTPStatus.UNAUTHORIZED}
        except Exception as e:
            return {"error":f"{str(e)}","status": HTTPStatus.INTERNAL_SERVER_ERROR}
    
    @blp.arguments(schema=Update())
    @jwt_required()
    @is_member
    def put(self, get_data,type,id):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                product_data = Inventory.query.filter_by(id=id).first()
                if product_data.products.name != type:
                    return {"error":"Your product id doesn't match your product type",'status': HTTPStatus.UNAUTHORIZED}
                if product_data == None:
                    return {"error":"The product id is not listed",'status': HTTPStatus.UNAUTHORIZED}
                
                if product_data.status != "active":
                    return {"error":"The product is not available",'status': HTTPStatus.UNAUTHORIZED}
                
                product_data.quantity = product_data.quantity + get_data.get('quantity')
                db.session.commit()

                return {"message":"Quanity of the product successfully updated.","status": HTTPStatus.OK}
            else:
                domain = domain[2]

                if type in domain:
                    product_data = Inventory.query.filter_by(id=id).first()
                    if product_data.products.name != type:
                        return {"error":"Your product id doesn't match your product type",'status': HTTPStatus.UNAUTHORIZED}
                    if product_data == None:
                        return {"error":"The product id is not listed",'status': HTTPStatus.UNAUTHORIZED}
                    
                    if product_data.status != "active":
                        return {"error":"The product is not available",'status': HTTPStatus.UNAUTHORIZED}
                    
                    product_data.quantity = product_data.quantity + get_data.get('quantity')
                    db.session.commit()

                    return {"message":"Quanity of the product successfully updated.","status": HTTPStatus.OK}
                else:
                    return {"error":"The product you are trying to update is out of your domain",'status': HTTPStatus.UNAUTHORIZED}
            
        except Exception as e:
            return {'error':f'{str(e)}','status':HTTPStatus.INTERNAL_SERVER_ERROR}
        
    @blp.arguments(schema=Delete())
    @jwt_required()
    @is_admin
    def delete(self, get_data,type,id):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                res = Inventory.query.filter_by(id=id).first()
                if res.products.name != type:
                    return {"error":"Your product id doesn't match your product type",'status': HTTPStatus.UNAUTHORIZED}
                if res == None:
                    return {"error":"The product id is not listed",'status': HTTPStatus.UNAUTHORIZED}
                
                res.status = get_data.get('status')
                db.session.commit()

                return {'message':'Product status successfully updated',"status": HTTPStatus.OK}
            else:
                domain = domain[2]

                if type in domain:
                    res = Inventory.query.filter_by(id=id).first()
                    if res.products.name != type:
                        return {"error":"Your product id doesn't match your product type",'status': HTTPStatus.UNAUTHORIZED}
                    if res == None:
                        return {"error":"The product id is not listed",'status': HTTPStatus.UNAUTHORIZED}
                    
                    res.status = get_data.get('status')
                    db.session.commit()

                    return {'message':'Product status successfully updated',"status": HTTPStatus.OK}
                else:
                    return {"error":"The product status you are trying to change is out of your domain",'status': HTTPStatus.UNAUTHORIZED}

        except Exception as e:
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}

blp.add_url_rule('/inventory/<type>/<id>', view_func=Inventory_Operations.as_view('Inventory_Operation'))

class ListProducts(MethodView):
    @blp.response(HTTPStatus.OK,schema=ProductResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self):
        try:
            res = Inventory.query.all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
blp.add_url_rule('/inventory', view_func=ListProducts.as_view('ListingOfProducts'))


@blp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}