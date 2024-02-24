from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token , jwt_required, get_jwt
import bcrypt
from http import HTTPStatus
from src.modules.user.models import User, Roles
from src.modules.product_type.models import Product_type
from src.service_modules.db.conn import db
from src.modules.user.parameter import SignupSchema, LoginSchema, ChangePasswordSchema, DeleteUserSchema, UpdateSchema, RoleAddSchema, RoleUpdateSchema
from src.modules.user.response import UserResponse, UserRolesResponse
from src.modules.user.blocklist import BlockList
from src.service_modules.auth import is_super_admin

blp = Blueprint('userinfo',__name__)
salt = bcrypt.gensalt()

class Login(MethodView):

    @blp.arguments(schema=LoginSchema())
    def post(self, req_data):
        try:
            res = User.query.filter_by(email=req_data.get('email')).first()
            role =Product_type.query.filter_by(id=res.role[0].product_type_id).all()
            email_exist = None
            if res != None:
                email_exist = res.password

            if email_exist is None or res.status == False:
                return {'error':'Email does not exist in the database','status': HTTPStatus.NOT_FOUND}

            stored_pass = email_exist.encode('utf-8')
            provided_pass = req_data.get('password').encode('utf-8')
            check_pass = bcrypt.checkpw(provided_pass, stored_pass)
            if not check_pass:
                return {'error':'Incorrect password','status': HTTPStatus.UNAUTHORIZED}
            roles = []
            for i in role:
                roles.append(i.name)
                
            token = create_access_token(identity= [req_data.get('email'), res.role[0].name, roles])
            print(token)

            return {"message":"Login successful",'status': HTTPStatus.OK}

        except Exception as e:
            return {'error': f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
blp.add_url_rule('/login', view_func=Login.as_view('Login'))

class Signup(MethodView):

    @blp.response(HTTPStatus.OK,schema=UserResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self,id):
        try:
            if id == 'all':
                res = User.query.all()
            else:
                res = User.query.filter_by(id = id).all()
            
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
    
    @blp.arguments(schema=SignupSchema())
    def post(self, req_data):
        try:
            hashed = bcrypt.hashpw(req_data.get('password').encode('utf-8'), salt)
            name = req_data.get('name').lower()
            
            entry = User(name=name, email=req_data.get('email'), password=hashed, status = True)
            db.session.add(entry)
            db.session.commit()
            return {"message":"User successfully registered.",'status': HTTPStatus.OK}
        except Exception as e:
            return {"error":f"{str(e)}",'status': HTTPStatus.INTERNAL_SERVER_ERROR}
    
    @blp.arguments(schema=ChangePasswordSchema())
    @jwt_required()
    def put(self, req_data):
        try:
            email = get_jwt()['sub']
                
            email_exist = User.query.filter_by(email=email[0]).first()

            stored_pass = email_exist.password.encode('utf-8')
            provided_pass = req_data.get('password').encode('utf-8')
            check_pass = bcrypt.checkpw(provided_pass, stored_pass)
            if not check_pass:
                return {'error':'Incorrect password','status': HTTPStatus.UNAUTHORIZED}
            
            if req_data.get('new_password') != req_data.get('confirm_password'):
                return {"error":"The new password and confirm password doesn't match",'status': HTTPStatus.BAD_REQUEST}
            
            hashed = bcrypt.hashpw(req_data.get('confirm_password').encode('utf-8'), salt)
            
            email_exist.password = hashed
            db.session.commit()

            return {'message': 'Password successfully changed','status': HTTPStatus.OK}
        except Exception as e:
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
    # @blp.arguments(schema=DeleteUserSchema())
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
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
        
blp.add_url_rule('/signup/<id>', view_func=Signup.as_view('SignUp'))


class Logout(MethodView):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt()['jti']
            BlockList.add(jti)
            return {"merssage":"Successfully Logged out",'status': HTTPStatus.OK}
        except Exception as e:
            return {'error': f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}

blp.add_url_rule('/logout', view_func=Logout.as_view('Logout'))

class RolesManagement(MethodView):

    @blp.response(HTTPStatus.OK,schema=UserRolesResponse(many=True))
    @jwt_required()
    @is_super_admin
    def get(self,id):
        try:
            if id == 'all':
                res = Roles.query.all()
            else:
                res = Roles.query.filter_by(id=id)
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
    
    @blp.arguments(schema=RoleAddSchema())
    @jwt_required()
    @is_super_admin
    def post(self, req_data):
        try:
            name = req_data.get('name')
            user = User.query.filter_by(id=req_data.get('user_id')).first()
            product_type = Product_type.query.filter_by(id=req_data.get('product_id')).first()
            if user.status == False:
                return {"error":"The user is deleted",'status': HTTPStatus.UNAUTHORIZED}
            entry = Roles(name=name, user=user, product_type=product_type)
            db.session.add(entry)
            db.session.commit()
            return {"message":"Role successfully registered.",'status': HTTPStatus.OK}
        except Exception as e:
            return {"error":f"{str(e)}",'status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
    @blp.arguments(schema=RoleUpdateSchema())
    @jwt_required()
    @is_super_admin
    def put(self, req_data,id):
        try:
            role = Roles.query.filter_by(id=id).first()
            user = User.query.filter_by(id = req_data.get('user_id')).first()
            if role == None:
                return {"error":"The role id you gave does not exist",'status': HTTPStatus.UNAUTHORIZED}
            if user == None:
                return {"error":"The user id you gave does not exist",'status': HTTPStatus.UNAUTHORIZED}
            if user.status == False:
                return {"error":"The user is deleted",'status': HTTPStatus.UNAUTHORIZED}
            role.user= user
            db.session.commit()
            return {"message":"Role successfully update.",'status': HTTPStatus.OK}
        except Exception as e:
            return {"error":f"{str(e)}",'status': HTTPStatus.INTERNAL_SERVER_ERROR}
        

blp.add_url_rule('/role/<id>', view_func=RolesManagement.as_view('RoleManagement'))

@blp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}

