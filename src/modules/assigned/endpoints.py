from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_
from src.service_modules.db.conn import db
from src.modules.assigned.models import Assigned
from src.modules.assigned.response import AssignedResponse
from src.modules.assigned.parameter import UpdateStatus
from datetime import datetime
from src.service_modules.auth import is_reader, is_member

api = Blueprint("assigned",__name__,description="Operations on Assigned products")

@api.route('/product_type/<product_type_id>/role/')
class Assigned(MethodView):

    @api.response(HTTPStatus.OK,schema=AssignedResponse(many=True))
    @jwt_required()
    @is_reader
    def get(self,product_type_id):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                res= Assigned.query.filter_by(product_type_id= int(product_type_id)).all()
            else:
                domain = domain[2]

                if int(product_type_id) in domain:
                    res= Assigned.query.filter_by(product_type_id= int(product_type_id)).all()

            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}

@api.route('/product_type/<product_type_id>/role/<id>')
class AssignedOperations(MethodView):

    @api.response(HTTPStatus.OK,schema=AssignedResponse(many=True))
    @jwt_required()
    @is_reader
    def get(self,product_type_id,id):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                res = Assigned.query.filter(
                        and_(
                            Assigned.id == int(id),
                            Assigned.product_type_id == int(product_type_id)
                        )).all()
            else:
                domain = domain[2]

                if int(product_type_id) in domain:
                    res = Assigned.query.filter(
                            and_(
                                Assigned.id == int(id),
                                Assigned.product_type_id == int(product_type_id)
                            )).all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}
    
    @api.arguments(schema=UpdateStatus())
    @jwt_required()
    @is_member
    def put(self,req_data,product_type_id,id):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                res =Assigned.query.filter(
                            and_(
                                Assigned.id == int(id),
                                Assigned.product_type_id == int(product_type_id)
                            )).first()
                if res == None:
                    raise Exception("There is no assigment with this id and product type id", HTTPStatus.NOT_FOUND)
                res.status = req_data.get('status')
                db.session.commit()
                return {'message': "Assigned product's status successfully changed.","status": HTTPStatus.OK}
            else:
                domain = domain[2]
                if int(product_type_id) in domain:
                    res = Assigned.query.filter(
                            and_(
                                Assigned.id == int(id),
                                Assigned.product_type_id == int(product_type_id)
                            )).first()
                    if res == None:
                        raise Exception("There is no assigment with this id and product type id", HTTPStatus.NOT_FOUND)
                    res.status = req_data.get('status')
                    db.session.commit()
                    return {'message': "Assigned product's status successfully changed.","status": HTTPStatus.OK}
                else:
                    raise Exception("The product type you are trying to access is out your domain", HTTPStatus.UNAUTHORIZED)
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1].value if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR.value
            return {'error': error_message, 'status': status_code}


@api.route('/product_type/<product_type_id>/product/<unique_code>')
class Assigned_History(MethodView):

    @api.response(HTTPStatus.OK,schema=AssignedResponse(many=True))
    @jwt_required()
    @is_reader
    def get(self,product_type_id,unique_code):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                res = Assigned.query.filter(
                        and_(
                            Assigned.unique_code == unique_code,
                            Assigned.product_type_id == int(product_type_id)
                        )).all()
            else:
                domain = domain[2]

                if int(product_type_id) in domain:
                    res = Assigned.query.filter(
                            and_(
                                Assigned.unique_code == unique_code,
                                Assigned.product_type_id == int(product_type_id)
                            )).all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}',"status": HTTPStatus.INTERNAL_SERVER_ERROR}
    
    @jwt_required()
    @is_member
    def put(self,product_type_id,unique_code):
        try:
            domain = get_jwt()['sub']
            role= domain[1]
            if role == 'super_admin':
                res =Assigned.query.filter(
                            and_(
                                Assigned.unique_code == unique_code,
                                Assigned.product_type_id == int(product_type_id)
                            )).first()
                if res == None:
                    raise Exception("There is no assigment with this unique code and product type id", HTTPStatus.NOT_FOUND)
                res.return_date = datetime.utcnow
                db.session.commit()
                return {'message': "Assigned product's return date successfully stored.","status": HTTPStatus.OK}
            else:
                domain = domain[2]
                if int(product_type_id) in domain:
                    res =Assigned.query.filter(
                            and_(
                                Assigned.unique_code == unique_code,
                                Assigned.product_type_id == int(product_type_id)
                            )).first()
                    if res == None:
                        raise Exception("There is no assigment with this unique code and product type id", HTTPStatus.NOT_FOUND)
                    res.return_date = datetime.utcnow
                    db.session.commit()
                    return {'message': "Assigned product's return date successfully stored.","status": HTTPStatus.OK}
                else:
                    raise Exception("The product type you are trying to access is out your domain", HTTPStatus.UNAUTHORIZED)
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1].value if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR.value
            return {'error': error_message, 'status': status_code}




@api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}