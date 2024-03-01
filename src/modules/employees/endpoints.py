from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from src.modules.employees.parameter import EmpAddchema
from src.modules.employees.response import EmployeeResponse
from src.modules.employees.models import Employee
from src.service_modules.db.conn import db
from src.service_modules.auth import is_super_admin

blp = Blueprint('employeeinfo',__name__)

class EmployeeOperations(MethodView):

    @blp.response(HTTPStatus.OK,schema=EmployeeResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self,id):
        try:
            if id == 'all':
                res = Employee.query.all()
            else:
                res = Employee.query.filter_by(id = id).all()
            
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
    
    @blp.arguments(schema=EmpAddchema())
    def post(self, req_data,id):
        try:
            name = req_data.get('name').lower()
            
            entry = Employee(name=name, email=req_data.get('email'),employee_id= req_data.get('employee_id'), status = True)
            db.session.add(entry)
            db.session.commit()
            return {"message":"Employee successfully registered.",'status': HTTPStatus.OK}
        except Exception as e:
            return {"error":f"{str(e)}",'status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
    @jwt_required()
    @is_super_admin
    def delete(self,id):
        try:
            res = Employee.query.filter_by(id=id).first()
            if res.status == True:
                res.status = False
            else:
                res.status = True
            db.session.commit()

            return {"message":"Employee's status sucessfully changed",'status': HTTPStatus.OK}
        except Exception as e:
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
        
blp.add_url_rule('/employee/<id>', view_func=EmployeeOperations.as_view('employeeOperations'))