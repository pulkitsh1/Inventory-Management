from flask import abort, Response
from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
import json, logging
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from src.service_modules.db.conn import db
from src.modules.inventory.models import Inventory
from src.modules.assigned.models import Assigned
from src.modules.employees.models import Employee
from src.modules.product_type.models import Product_type
from src.modules.inventory.parameter import Product, Update, Delete
from src.modules.inventory.response import ProductResponse
from src.service_modules.auth import is_admin,is_member,is_reader,is_super_admin
from src.utils.constants import Constants

api = Blueprint("inventory",__name__,description="Operations on Inventory")

@api.route('/product_type/<product_type_id>/inventory/')
class InventoryOperations(MethodView):

    @api.response(HTTPStatus.OK,schema=ProductResponse(many=True))
    @jwt_required()
    @is_reader
    def get(self,product_type_id):
        try:
            domain = get_jwt()['sub']
            role= domain['role']
            if role == Constants.super_role.value:
                res = Inventory.query.filter_by(product_type_id=product_type_id).all()
            else:
                domain = domain['domain']
                if int(product_type_id) in domain:
                    res = Inventory.query.filter_by(product_type_id=product_type_id).all()

            return res
        
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
        
    @api.arguments(schema=Product())
    @jwt_required()
    @is_admin
    def post(self, req_data,product_type_id):
        try:
            domain = get_jwt()['sub']
            role= domain['role']
            if role == Constants.super_role.value:
                res = Product_type.query.filter_by(id=int(product_type_id)).first()
                if res == None:
                    raise Exception("No product type exists by this id",HTTPStatus.NOT_FOUND)
                product_name = req_data.get('product_name').lower()
                entry = Inventory(product_name=product_name, price=req_data.get('price'), quantity=req_data.get('quantity'), products=res, status = "active")
                db.session.add(entry)
                db.session.commit()
                return {"message":"Product added successfully.","status": HTTPStatus.OK}
            else:
                domain = domain['domain']

                if int(product_type_id) in domain:
                    res = Product_type.query.filter_by(id=int(product_type_id)).first()
                    if res == None:
                        raise Exception("No product type exists by this id", HTTPStatus.NOT_FOUND)
                    product_name = req_data.get('product_name').lower()
                    entry = Inventory(product_name=product_name, price=req_data.get('price'), quantity=req_data.get('quantity'), products=res, status = "active")
                    db.session.add(entry)
                    db.session.commit()
                    return {"message":"Product added successfully.","status": HTTPStatus.OK}
                else:
                    raise Exception("The product type you are trying to add is out of your domain", HTTPStatus.UNAUTHORIZED)
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))

@api.route('/product_type/<product_type_id>/inventory/<id>')
class ProductInventory(MethodView):

    @api.response(HTTPStatus.OK,schema=ProductResponse(many=True))
    @jwt_required()
    @is_reader
    def get(self,product_type_id,id):
        try:
            domain = get_jwt()['sub']
            role= domain['role']
            if role == Constants.super_role.value:
                res = Inventory.query.filter_by(id=id).all()
                if res[0].products.id != int(product_type_id):
                        res = []
            else:
                domain = domain['domain']

                if int(product_type_id) in domain:
                    res = Inventory.query.filter_by(id=id).all()
                    if res[0].products.name != int(product_type_id):
                        res = []
            return res
        
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
    
    @api.arguments(schema=Update())
    @jwt_required()
    @is_member
    def put(self, get_data,product_type_id,id):
        try:
            domain = get_jwt()['sub']
            role= domain['role']
            if role == Constants.super_role.value:
                product_data = Inventory.query.filter_by(id=id).first()
                if product_data == None:
                    raise Exception("The product id is not listed")
                
                if product_data.status != Constants.active_status.value:
                    raise Exception("The product is not available")
                
                product_data.quantity = product_data.quantity - get_data.get('quantity')
                emp_data = Employee.query.filter_by(id=get_data.get('emp_id')).first()
                type_id = Product_type.query.filter_by(id=product_data.product_type_id).first()
                if type_id.name != Constants.type_it.value:
                    entry = Assigned(product=product_data,employee=emp_data, quantity=get_data.get('quantity'),product_type= type_id ,status= 'ok')
                else:
                    entry = Assigned(product=product_data,employee=emp_data, quantity=get_data.get('quantity'),product_type= type_id,unique_code=get_data.get('unique_code') ,status= 'ok')
                db.session.add(entry)
                db.session.commit()

                return {"message":"Quanity of the product successfully updated.","status": HTTPStatus.OK}
            else:
                domain = domain['domain']

                if int(product_type_id) in domain:
                    product_data = Inventory.query.filter_by(id=id).first()
                    if product_data.product_type_id != int(product_type_id):
                        raise Exception("Your product id doesn't match your product type", HTTPStatus.UNAUTHORIZED)
                    if product_data == None:
                        raise Exception("The product id is not listed", HTTPStatus.NOT_FOUND)
                
                    if product_data.status != Constants.active_status.value:
                        raise Exception("The product is not available",HTTPStatus.NOT_FOUND)
                    
                    product_data.quantity = product_data.quantity - get_data.get('quantity')
                    emp_data = Employee.query.filter_by(id=get_data.get('emp_id')).first()
                    type_id = Product_type.query.filter_by(id=product_data.product_type_id).first()
                    if type_id.name != Constants.type_it.value:
                        entry = Assigned(product=product_data,employee=emp_data, quantity=get_data.get('quantity'),product_type= type_id ,status= 'ok')
                    else:
                        entry = Assigned(product=product_data,employee=emp_data, quantity=get_data.get('quantity'),product_type= type_id,unique_code=get_data.get('unique_code') ,status= 'ok')
                    db.session.add(entry)
                    db.session.commit()

                    return {"message":"Quanity of the product successfully updated.","status": HTTPStatus.OK}
                else:
                    raise Exception("The product you are trying to update is out of your domain", HTTPStatus.UNAUTHORIZED)
            
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
        
    @api.arguments(schema=Delete())
    @jwt_required()
    @is_admin
    def delete(self, get_data,product_type_id,id):
        try:
            domain = get_jwt()['sub']
            role= domain['role']
            if role == Constants.super_role.value:
                res = Inventory.query.filter_by(id=id).first()
                if res.product_type_id != int(product_type_id):
                    raise Exception("Your product id doesn't match your product type", HTTPStatus.UNAUTHORIZED)
                if res == None:
                    raise Exception("The product id is not listed", HTTPStatus.NOT_FOUND)
                
                res.status = get_data.get('status')
                db.session.commit()

                return {'message':'Product status successfully updated',"status": HTTPStatus.OK}
            else:
                domain = domain['domain']

                if int(product_type_id) in domain:
                    res = Inventory.query.filter_by(id=id).first()
                    if res.product_type_id != int(product_type_id):
                        raise Exception("Your product id doesn't match your product type", HTTPStatus.UNAUTHORIZED)
                    if res == None:
                        raise Exception("The product id is not listed", HTTPStatus.NOT_FOUND)
                    
                    res.status = get_data.get('status')
                    db.session.commit()

                    return {'message':'Product status successfully updated',"status": HTTPStatus.OK}
                else:
                    raise Exception("The product status you are trying to change is out of your domain", HTTPStatus.UNAUTHORIZED)

        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))



@api.route('/inventory')
class ListProducts(MethodView):
    @api.response(HTTPStatus.OK,schema=ProductResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self):
        try:
            res = Inventory.query.all()
            return res
        
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
        

@api.route('/product_type/<product_type_id>/countofproducts/inventory/<id>')
class CountOfProducts(MethodView):
    @jwt_required()
    @is_reader
    def get(self,product_type_id,id):
        try:
            domain = get_jwt()['sub']
            role= domain['role']
            if role == Constants.super_role.value:
                res = Inventory.query.filter_by(id=id).first()
                total = 0
                for i in res.assigned:
                    total = total + i.quantity
                overalltotal = total+res.quantity
                res = {
                    "Total":overalltotal,
                    "Available":res.quantity,
                    "Used":total,
                    "product_id":int(id),
                    "product_type_id": res.product_type_id
                }
            else:
                domain = domain['domain']

                if int(product_type_id) in domain:
                    res = Inventory.query.filter_by(id=id).first()
                total = 0
                for i in res.assigned:
                    total = total + i.quantity
                total = total+res.quantity
                res = {
                    "Total":overalltotal,
                    "Available":res.quantity,
                    "Used":total,
                    "product_id":int(id),
                    "product_type_id": res.product_type_id
                }
            return res
        
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
        

@api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}