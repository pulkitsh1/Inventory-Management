import string
import random
import os
from werkzeug.utils import secure_filename
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_
from src.service_modules.db.conn import db
from src.modules.transactions.models import TransactionsModel
from src.modules.inventory.models import Inventory
from src.modules.product_type.models import Product_type
from src.modules.transactions.parameter import TransactionSchema
from src.modules.transactions.response import TransactionResponse
from src.service_modules.auth import is_admin,is_member,is_reader,is_super_admin
from src.utils.helper import *

api = Blueprint("transactions",__name__,description="Operations related Transactions")

@api.route('/product_type/<product_type_id>/transaction/')
class Transaction(MethodView):

    @api.response(HTTPStatus.OK,schema=TransactionResponse(many=True))
    @jwt_required()
    @is_reader
    def get(self,product_type_id):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                     res = Product_type.query.filter_by(id = int(product_type_id)).first()
                     res = TransactionsModel.query.filter_by(product_type= res.name).all()
            else:
                domain = domain[2]
                if int(product_type_id) in domain:
                    res = Product_type.query.filter_by(id = int(product_type_id)).first()
                    res = TransactionsModel.query.filter_by(product_type= res.name).all()

        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
    @api.arguments(schema=TransactionSchema())
    @jwt_required()
    @is_admin
    def post(self,req_data,product_type_id,transactionid):
        try:
            # schema = TransactionSchema()
            # req_data = schema.load(request.form)
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                # print(request.files.get('attachments'))
                # file = request.files.get('attachments')
                # print(file.filename)
                # if file.filename == '':
                #     raise Exception("No file present in attachment.", HTTPStatus.NOT_FOUND)
                # temp=file.filename.rsplit('.',1)
                # temp= temp[1]
                # print(temp)
                # name = ''.join(random.choices(string.ascii_lowercase +
                #              string.digits, k=12))
                # file.filename = str(name) + "." + temp
                # print(file.filename)
                # if file_valid(file.filename):
                #     filename = secure_filename(file.filename)
                #     print(filename)
                #     print(UPLOAD_FOLDER)
                #     file.save(os.path.join(UPLOAD_FOLDER),filename)
                # res = Product_type.query.filter_by(id = int(product_type_id)).first()
                entry = TransactionsModel(product_name= req_data.get('product_name'), price_per_unit= req_data.get('price_per_unit'),
                                    total_price= req_data.get('total_price'), quantity=req_data.get('quantity'), product_type=res.name,
                                    transaction_id= transactionid, order_status= 'order placed')
                db.session.add(entry)
                db.session.commit()
                return {"message":"Transaction recorded successfully.","status": HTTPStatus.OK}
            else:
                domain = domain[2]
                if int(product_type_id) in domain:
                    res = Product_type.query.filter_by(id = int(product_type_id)).first()
                    entry = TransactionsModel(product_name= req_data.get('product_name'), price_per_unit= req_data.get('price_per_unit'),
                                        total_price= req_data.get('total_price'), quantity=req_data.get('quantity'), product_type=res.name,
                                        transaction_id= transactionid, order_status= 'order placed')
                    db.session.add(entry)
                    db.session.commit()
                    return {"message":"Transaction recorded successfully.","status": HTTPStatus.OK}
                else:
                    raise Exception("This product type is out of your domain",HTTPStatus.UNAUTHORIZED)
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1].value if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR.value
            return {'error': error_message, 'status': status_code}

@api.route('/product_type/<product_type_id>/transaction/<transactionid>')
class TransactionOperations(MethodView):

    @api.response(HTTPStatus.OK,schema=TransactionResponse(many=True))
    @jwt_required()
    @is_reader
    def get(self,product_type_id,transactionid):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                res = Product_type.query.filter_by(id = int(product_type_id)).first()
                res = TransactionsModel.query.filter(
                        and_(
                            TransactionsModel.transaction_id == transactionid,
                            TransactionsModel.product_type == res.name
                        )
                    ).all()
            else:
                domain = domain[2]
                if int(product_type_id) in domain:
                    res = Product_type.query.filter_by(id = int(product_type_id)).first()
                    res = TransactionsModel.query.filter(
                            and_(
                                TransactionsModel.transaction_id == transactionid,
                                TransactionsModel.product_type == res.name
                            )
                        ).all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
    # @api.arguments(schema=TransactionIDSchema())
    @jwt_required()
    @is_member
    def put(self,product_type_id,transactionid):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                res = TransactionsModel.query.filter_by(transaction_id= transactionid).first()
                res.order_status = 'Delivered'
                quantity = res.quantity
                adjust = Inventory.query.filter_by(product_name= res.product_name).first()
                if adjust != None:
                    adjust.quantity = adjust.quantity + quantity
                else:
                    product_name = res.product_name.lower()
                    entry = Inventory(product_name= product_name, price=res.price_per_unit, quantity=res.quantity, product_type=res.product_type)
                    db.session.add(entry)
                db.session.commit()
                return {"message":"Quanity of the product successfully updated.","status": HTTPStatus.OK}
            else:
                domain = domain[2]

                if int(product_type_id) in domain:
                    res = TransactionsModel.query.filter_by(transaction_id= transactionid).first()
                    res.order_status = 'Delivered'
                    quantity = res.quantity
                    adjust = Inventory.query.filter_by(product_name= res.product_name).first()
                    if adjust != None:
                        adjust.quantity = adjust.quantity + quantity
                    else:
                        product_name = res.product_name.lower()
                        entry = Inventory(product_name= product_name, price=res.price_per_unit, quantity=res.quantity, product_type=res.product_type)
                        db.session.add(entry)
                    db.session.commit()
                    return {"message":"Quanity of the product successfully updated.","status": HTTPStatus.OK}
                else:
                    raise Exception("This product type is out of your domain", HTTPStatus.UNAUTHORIZED)
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1].value if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR.value
            return {'error': error_message, 'status': status_code}
        

@api.route('/transactions')
class Transactions(MethodView):

    # @api.arguments(schema=TransactionIDSchema())
    @api.response(HTTPStatus.OK,schema=TransactionResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self):
        try:
            res = TransactionsModel.query.all()
            return res
        except Exception as e:
            return {"error":f"{str(e)}","status": HTTPStatus.INTERNAL_SERVER_ERROR}
        

@api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}