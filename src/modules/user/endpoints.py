from flask import abort, Response
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token , jwt_required, get_jwt
import bcrypt
from http import HTTPStatus
from src.modules.user.models import User, Roles
from src.modules.product_type.models import Product_type
from src.modules.employees.models import Employee
from src.service_modules.db.conn import db
from src.modules.user.parameter import SignupSchema, LoginSchema, ChangePasswordSchema, RoleAddSchema, RoleUpdateSchema
from src.modules.user.response import UserResponse, UserRolesResponse
from src.service_modules.auth import is_super_admin
import config
import json

api = Blueprint("userinfo",__name__,description="Operations on Users")
salt = bcrypt.gensalt()

@api.route('/login')
class Login(MethodView):

    @api.arguments(schema=LoginSchema())
    def post(self, req_data):
        try:
            res = User.query.filter_by(email=req_data.get('email')).first()
            email_exist = None
            if res != None:
                email_exist = res.password
                
            if email_exist is None or res.status == False:
                raise Exception('Email does not exist in the database', HTTPStatus.UNAUTHORIZED)
            
            stored_pass = email_exist.encode('utf-8')
            provided_pass = req_data.get('password').encode('utf-8')
            check_pass = bcrypt.checkpw(provided_pass, stored_pass)
            if not check_pass:
                raise Exception('Incorrect password',HTTPStatus.UNAUTHORIZED)
            role =Product_type.query.filter_by(id=res.role[0].product_type_id).all()
            roles = []
            for i in role:
                roles.append(i.id)
                
            # token = create_access_token(identity= [req_data.get('email'), res.role[0].name, roles])
            token = create_access_token(identity= {'email':req_data.get('email'),'role':res.role[0].name,'domain':roles})
            
            return ({"message":"Login successful","jwt_token":token,'status': HTTPStatus.OK}),200

        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))

@api.route('/signup/')
class Signup(MethodView):

    @api.response(HTTPStatus.OK,schema=UserResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self):
        try:
            res = User.query.all()

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
        
    @api.arguments(schema=SignupSchema())
    def post(self, req_data):
        try:
            hashed = bcrypt.hashpw(req_data.get('password').encode('utf-8'), salt)
            name = req_data.get('name').lower()
            if req_data.get('password') != req_data.get('confirm_password'):
                raise Exception("Password and Confirm Password doesn't match.", HTTPStatus.UNAUTHORIZED)
            
            entry = User(name=name, email=req_data.get('email'), password=hashed, status = True)
            emp_entry = Employee(name=name,email=req_data.get('email'),status = True)
            db.session.add(entry)
            db.session.add(emp_entry)
            db.session.commit()
            return {"message":"User successfully registered.",'status': HTTPStatus.OK}
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
        
    @api.arguments(schema=ChangePasswordSchema())
    @jwt_required()
    def put(self, req_data):
        try:
            email = get_jwt()['sub']
            email = email['email']

            email_exist = User.query.filter_by(email=email).first()
            
            stored_pass = email_exist.password.encode('utf-8')
            provided_pass = req_data.get('password').encode('utf-8')
            check_pass = bcrypt.checkpw(provided_pass, stored_pass)
            if not check_pass:
                raise Exception('Incorrect password', HTTPStatus.UNAUTHORIZED)
            
            if req_data.get('new_password') != req_data.get('confirm_password'):
                raise Exception("The new password and confirm password doesn't match", HTTPStatus.UNAUTHORIZED)
            
            hashed = bcrypt.hashpw(req_data.get('confirm_password').encode('utf-8'), salt)
            
            email_exist.password = hashed
            db.session.commit()

            return {'message': 'Password successfully changed','status': HTTPStatus.OK}
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))

@api.route('/signup/<id>')
class UserOperations(MethodView):

    @api.response(HTTPStatus.OK,schema=UserResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self,id):
        try:
            res = User.query.filter_by(id = id).all()
            
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

        
    # @api.arguments(schema=DeleteUserSchema())
    @jwt_required()
    @is_super_admin
    def delete(self,id):
        try:
            res = User.query.filter_by(id=id).first()
            if res.status == True:
                res.status = False
            else:
                res.status = True
            db.session.commit()

            return {"message":"User's status sucessfully changed",'status': HTTPStatus.OK}
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
        

@api.route('/logout')
class Logout(MethodView):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt()["jti"]
            config.jwt_redis_blocklist.set(jti, "", ex=config.ACCESS_EXPIRES)
            return {"merssage":"Successfully Logged out",'status': HTTPStatus.OK}
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
        
@api.route('/role/')
class Roles(MethodView):

    @api.response(HTTPStatus.OK,schema=UserRolesResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self):
        try:
            res = Roles.query.all()
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
        
    @api.arguments(schema=RoleAddSchema())
    @jwt_required()
    @is_super_admin
    def post(self, req_data):
        try:
            name = req_data.get('name')
            user = User.query.filter_by(id=req_data.get('user_id')).first()
            product_type = Product_type.query.filter_by(id=req_data.get('product_id')).first()
            if user.status == False:
                raise Exception("The user is deleted", HTTPStatus.NOT_FOUND)
            entry = Roles(name=name, user=user, product_type=product_type)
            db.session.add(entry)
            db.session.commit()
            return {"message":"Role successfully registered.",'status': HTTPStatus.OK}
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))

@api.route('/role/<id>')
class RolesManagement(MethodView):

    @api.response(HTTPStatus.OK,schema=UserRolesResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self,id):
        try:
            res = Roles.query.filter_by(id=id)
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
        
    @api.arguments(schema=RoleUpdateSchema())
    @jwt_required()
    @is_super_admin
    def put(self, req_data,id):
        try:
            role = Roles.query.filter_by(id=id).first()
            user = User.query.filter_by(id = req_data.get('user_id')).first()
            if role == None:
                raise Exception("The role id you gave does not exist",HTTPStatus.NOT_FOUND)
            if user == None:
                raise Exception("The user id you gave does not exist", HTTPStatus.NOT_FOUND)
            if user.status == False:
                raise Exception("The user is deleted",HTTPStatus.NOT_FOUND)
            role.user= user
            db.session.commit()
            return {"message":"Role successfully update.",'status': HTTPStatus.OK}
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

