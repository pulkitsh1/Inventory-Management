from flask import abort, Response
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from http import HTTPStatus
import json
from src.modules.employees.parameter import EmpAddchema
from src.modules.employees.response import EmployeeResponse
from src.modules.employees.models import Employee
from src.service_modules.db.conn import db
from src.service_modules.auth import is_super_admin

api = Blueprint("employeeinfo",__name__,description="Operations on employees")

@api.route('/employee/')
class Employee(MethodView):

    @api.response(HTTPStatus.OK,schema=EmployeeResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self):
        try:
            res = Employee.query.all()
            return res
        
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
        
    @api.arguments(schema=EmpAddchema())
    def post(self, req_data):
        try:
            name = req_data.get('name').lower()
        
            entry = Employee(name=name, email=req_data.get('email'),employee_id= req_data.get('employee_id'), status = True)
            db.session.add(entry)
            db.session.commit()
            
            return {"message":"Employee successfully registered.",'status': HTTPStatus.OK}
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))

@api.route('/employee/<id>')
class EmployeeOperations(MethodView):

    @api.response(HTTPStatus.OK,schema=EmployeeResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self,id):
        try:
            res = Employee.query.filter_by(id = id).all()
            return res
        
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
        
    @jwt_required()
    @is_super_admin
    def delete(self,id):
        try:
            res = Employee.query.filter_by(id=id).first()
            if res == None:
                raise Exception("There is no employee by the given id", HTTPStatus.NOT_FOUND)
            
            if res.status == True:
                res.status = False
            else:
                res.status = True
            db.session.commit()

            return {"message":"Employee's status sucessfully changed",'status': HTTPStatus.OK}
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
        
        
@api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}