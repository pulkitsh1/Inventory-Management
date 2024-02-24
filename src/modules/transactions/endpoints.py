from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_
from src.service_modules.db.conn import db
from src.modules.transactions.models import TransactionsModel
from src.modules.inventory.models import Inventory
from src.modules.transactions.parameter import TransactionSchema, TransactionIDSchema
from src.modules.transactions.response import TransactionResponse
from src.service_modules.auth import is_admin,is_member,is_reader,is_super_admin

blp = Blueprint('transactions',__name__)

class Transaction(MethodView):

    @blp.response(HTTPStatus.OK,schema=TransactionResponse(many=True))
    @jwt_required()
    @is_reader
    def get(self,type,transactionid):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                if transactionid == 'all':
                     res = TransactionsModel.query.filter_by(product_type= type).all()
                else:
                    res = TransactionsModel.query.filter(
                            and_(
                                TransactionsModel.transaction_id == transactionid,
                                TransactionsModel.product_type == type
                            )
                        ).all()
            else:
                domain = domain[2]
                if type in domain:
                    if transactionid == 'all':
                        res = TransactionsModel.query.filter_by(product_type= type).all()
                    else:
                        res = TransactionsModel.query.filter(
                                and_(
                                    TransactionsModel.transaction_id == transactionid,
                                    TransactionsModel.product_type == type
                                )
                            ).all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}

    @blp.arguments(schema=TransactionSchema())
    @jwt_required()
    @is_admin
    def post(self, req_data,type,transactionid):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                entry = TransactionsModel(product_name= req_data.get('product_name'), price_per_unit= req_data.get('price_per_unit'),
                                    total_price= req_data.get('total_price'), quantity=req_data.get('quantity'), product_type=type,
                                    transaction_id= transactionid, order_status= 'order placed')
                db.session.add(entry)
                db.session.commit()
                return {"message":"Transaction recorded successfully.","status": HTTPStatus.OK}
            else:
                domain = domain[2]
                if type in domain:
                    entry = TransactionsModel(product_name= req_data.get('product_name'), price_per_unit= req_data.get('price_per_unit'),
                                        total_price= req_data.get('total_price'), quantity=req_data.get('quantity'), product_type=type,
                                        transaction_id= transactionid, order_status= 'order placed')
                    db.session.add(entry)
                    db.session.commit()
                    return {"message":"Transaction recorded successfully.","status": HTTPStatus.OK}
                else:
                    return {"error":"This product type is out of your domain",'status': HTTPStatus.UNAUTHORIZED}
        except Exception as e:
            return {"error":f"{str(e)}","status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
    # @blp.arguments(schema=TransactionIDSchema())
    @jwt_required()
    @is_member
    def put(self,type,transactionid):
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

                if type in domain:
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
                    return {"error":"This product type is out of your domain",'status': HTTPStatus.UNAUTHORIZED}
        except Exception as e:
            return {"error":f"{str(e)}","status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
blp.add_url_rule('/transactions/<type>/<transactionid>', view_func=Transaction.as_view('Transaction'))

class Transactions(MethodView):

    # @blp.arguments(schema=TransactionIDSchema())
    @blp.response(HTTPStatus.OK,schema=TransactionResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self):
        try:
            res = TransactionsModel.query.all()
            return res
        except Exception as e:
            return {"error":f"{str(e)}","status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
        
blp.add_url_rule('/transactions', view_func=Transactions.as_view('Transactions'))

@blp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}