from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from src.service_modules.db.conn import db
from src.modules.user.models import User
from src.modules.transactions.models import TransactionsModel
from src.modules.inventory.models import Inventory
from src.modules.transactions.parameter import TransactionSchema, TransactionIDSchema
from src.modules.transactions.response import TransactionResponse

blp = Blueprint('transactions',__name__)

class Transaction(MethodView):

    @blp.response(HTTPStatus.OK,schema=TransactionResponse(many=True))
    @jwt_required()
    def get(self):
        try:
            email = get_jwt()['sub']
            email_exist = User.query.filter_by(email=email).first()
            type = email_exist.product_type

            res = TransactionsModel.query.filter_by(product_type=type).all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}

    @blp.arguments(schema=TransactionSchema())
    @jwt_required()
    def post(self, req_data):
        try:
            email = get_jwt()['sub']
            email_exist = User.query.filter_by(email=email).first()
            type = email_exist.product_type

            entry = TransactionsModel(product_name= req_data.get('product_name'), price_per_unit= req_data.get('price_per_unit'),
                                total_price= req_data.get('total_price'), quantity=req_data.get('quantity'), product_type=type,
                                transaction_id= req_data.get('transaction_id'), order_status= 'order placed')
            db.session.add(entry)
            db.session.commit()
            return {"message":"Transaction recorded successfully.","status": HTTPStatus.OK}
        except Exception as e:
            return {"error":f"{str(e)}","status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
    @blp.arguments(schema=TransactionIDSchema())
    @jwt_required()
    def put(self, req_data):
        try:
            res = TransactionsModel.query.filter_by(transaction_id= req_data.get('transaction_id')).first()
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
        except Exception as e:
            return {"error":f"{str(e)}","status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
blp.add_url_rule('/transactions', view_func=Transaction.as_view('Transaction'))

class TransactionID(MethodView):

    @blp.arguments(schema=TransactionIDSchema())
    @blp.response(HTTPStatus.OK,schema=TransactionResponse())
    @jwt_required()
    def post(self, req_data):
        try:
            res = TransactionsModel.query.filter_by(transaction_id= req_data.get('transaction_id')).first()
            return res
        except Exception as e:
            return {"error":f"{str(e)}","status": HTTPStatus.INTERNAL_SERVER_ERROR}
        
        
blp.add_url_rule('/transactionid', view_func=TransactionID.as_view('TransactionId'))

@blp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}