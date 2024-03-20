import string
import random
import os
from werkzeug.utils import secure_filename
from flask import request, send_file
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
from config import *
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
            print(role)
            if role == 'super_admin':
                     print("hjbgjhg")
                     res = Product_type.query.filter_by(id = int(product_type_id)).first()
                     print(res)
                     res = TransactionsModel.query.filter_by(product_type= res.name).all()
                     print(res)
            else:
                domain = domain[2]
                if int(product_type_id) in domain:
                    res = Product_type.query.filter_by(id = int(product_type_id)).first()
                    res = TransactionsModel.query.filter_by(product_type= res.name).all()
            return res
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
    # @api.arguments(schema=TransactionSchema())
    @jwt_required()
    @is_admin
    def post(self,product_type_id):
        try:
            schema = TransactionSchema()
            req_data = schema.load(request.form)
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                files = request.files.getlist('attachments')
                files_name = ''
                # file_size = files.read()
                # print("file size ", len(file_size)/1024)
                total_size = 0
                for file in files:
                    if file.filename == '':
                        raise Exception("No file present in attachment.", HTTPStatus.NOT_FOUND)
                    file.flush()
                    size = os.fstat(file.fileno()).st_size
                    total_size = total_size + size
                print(total_size)
                if not total_size <= int(ATTACHMENT_MAX_SIZE):
                    raise Exception("Attachments size has exceeded the limit of 10 MB.", HTTPStatus.NOT_FOUND)
                for file in files:
                    temp=file.filename.rsplit('.',1)
                    temp= temp[1]
                    name = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=25))
                    file.filename = str(name) + "." + temp
                    if file_valid(file.filename):
                        filename = secure_filename(file.filename)
                        files_name = files_name + filename + ','
                        file.save(os.path.join(os.sep, UPLOAD_FOLDER ,filename))
                res = Product_type.query.filter_by(id = int(product_type_id)).first()
                entry = TransactionsModel(product_name= req_data.get('product_name'), price_per_unit= req_data.get('price_per_unit'),
                                    total_price= req_data.get('total_price'), quantity=req_data.get('quantity'), product_type=res.name,
                                    transaction_id= req_data.get('transaction_id'), order_status= 'order placed', attachments = files_name, attachments_count=len(files))
                db.session.add(entry)
                db.session.commit()
                return {"message":"Transaction recorded successfully.","status": HTTPStatus.OK}
            else:
                domain = domain[2]
                if int(product_type_id) in domain:
                    files = request.files.getlist('attachments')
                    files_name = ''
                    # file_size = files.read()
                    # print("file size ", len(file_size)/1024)
                    total_size = 0
                    for file in files:
                        if file.filename == '':
                            raise Exception("No file present in attachment.", HTTPStatus.NOT_FOUND)
                        file.flush()
                        size = os.fstat(file.fileno()).st_size
                        total_size = total_size + size
                    print(total_size)
                    if not total_size <= int(ATTACHMENT_MAX_SIZE):
                        raise Exception("Attachments size has exceeded the limit of 10 MB.", HTTPStatus.NOT_FOUND)
                    for file in files:
                        temp=file.filename.rsplit('.',1)
                        temp= temp[1]
                        name = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=25))
                        file.filename = str(name) + "." + temp
                        if file_valid(file.filename):
                            filename = secure_filename(file.filename)
                            files_name = files_name + filename + ','
                            file.save(os.path.join(os.sep, UPLOAD_FOLDER ,filename))
                    res = Product_type.query.filter_by(id = int(product_type_id)).first()
                    entry = TransactionsModel(product_name= req_data.get('product_name'), price_per_unit= req_data.get('price_per_unit'),
                                        total_price= req_data.get('total_price'), quantity=req_data.get('quantity'), product_type=res.name,
                                        transaction_id= req_data.get('transaction_id'), order_status= 'order placed', attachments = filename)
                    db.session.add(entry)
                    db.session.commit()
                    return {"message":"Transaction recorded successfully.","status": HTTPStatus.OK}
                else:
                    raise Exception("This product type is out of your domain",HTTPStatus.UNAUTHORIZED)
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
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
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
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
        
@api.route('/product_type/<product_type_id>/attachments/transaction/<transactionid>')
class Get_Attachment(MethodView):
    @jwt_required()
    @is_reader
    def get(self, product_type_id,transactionid):
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
                        ).first()
                res = res.attachments.split(",")
                res.pop()
            else:
                domain = domain[2]
                if int(product_type_id) in domain:
                    res = Product_type.query.filter_by(id = int(product_type_id)).first()
                    res = TransactionsModel.query.filter(
                                and_(
                                    TransactionsModel.transaction_id == transactionid,
                                    TransactionsModel.product_type == res.name
                                )
                            ).first()
                    res = res.attachments.split(",")
                    res.pop()
            return res
        except Exception as e:
            return {"error":f"{str(e)}","status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
@api.route('/attachment/transaction/<path:filename>')
class Get_Attachment(MethodView):
    @jwt_required()
    @is_reader
    def get(self,filename):
        try:
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            return send_file(file_path)
        except Exception as e:
            return {"error":f"{str(e)}","status": HTTPStatus.INTERNAL_SERVER_ERROR}
        

@api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}