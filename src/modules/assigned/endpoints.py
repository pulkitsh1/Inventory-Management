from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_
from src.service_modules.db.conn import db
from src.modules.assigned.models import Assigned
from src.modules.assigned.response import AssignedResponse
from src.modules.assigned.parameter import Update
from src.service_modules.auth import is_reader

api = Blueprint('assigned',__name__)

class Assigned_Operations(MethodView):

    @api.response(HTTPStatus.OK,schema=AssignedResponse(many=True))
    @jwt_required()
    @is_reader
    def get(self,product_type_id,id):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                if id == 'all':
                    res= Assigned.query.filter_by(product_type_id= int(product_type_id)).all()
                else:
                    res = Assigned.query.filter(
                            and_(
                                Assigned.id == id,
                                Assigned.product_type_id == int(product_type_id)
                            )).all()
            else:
                domain = domain[2]

                if int(product_type_id) in domain:
                    if id == 'all':
                        res= Assigned.query.filter_by(product_type_id= int(product_type_id)).all()
                else:
                    res = Assigned.query.filter(
                            and_(
                                Assigned.id == id,
                                Assigned.product_type_id == int(product_type_id)
                            )).all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}
    
    @api.arguments(schema=Update())
    @jwt_required()
    def put(self,req_data,product_type_id,id):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                res =Assigned.query.filter(
                            and_(
                                Assigned.id == id,
                                Assigned.product_type_id == int(product_type_id)
                            )).first()
                res.status = req_data.get('status')
                db.session.commit()
                return {'message': "Assigned product's status successfully changed.","status": HTTPStatus.OK}
            else:
                domain = domain[2]
                if int(product_type_id) in domain:
                    res = Assigned.query.filter(
                            and_(
                                Assigned.id == id,
                                Assigned.product_type_id == int(product_type_id)
                            )).first()
                    res.status = req_data.get('status')
                    db.session.commit()
                    return {'message': "Assigned product's status successfully changed.","status": HTTPStatus.OK}
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}
api.add_url_rule('/assigned/<id>/product_type/<product_type_id>', view_func=Assigned_Operations.as_view('Assigned_Operations'))

@api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}