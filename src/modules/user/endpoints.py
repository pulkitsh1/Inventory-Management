from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token , jwt_required, get_jwt
import bcrypt
from http import HTTPStatus
from src.modules.user.models import User
from src.service_modules.db.conn import db
from src.modules.user.parameter import SignupSchema, LoginSchema, ChangePasswordSchema, DeleteUserSchema, UpdateSchema
from src.modules.user.response import UserResponse
from src.modules.user.blocklist import BlockList

blp = Blueprint('userinfo',__name__)
salt = bcrypt.gensalt()

class Login(MethodView):

    @blp.arguments(schema=LoginSchema())
    def post(self, req_data):
        try:
            res = User.query.filter_by(email=req_data.get('email')).first()
            email_exist = None
            if res != None:
                email_exist = res.password

            if email_exist is None:
                return {'error':'Email does not exist in the database','status': HTTPStatus.NOT_FOUND}

            stored_pass = email_exist.encode('utf-8')
            provided_pass = req_data.get('password').encode('utf-8')
            check_pass = bcrypt.checkpw(provided_pass, stored_pass)
            if not check_pass:
                return {'error':'Incorrect password','status': HTTPStatus.UNAUTHORIZED}
            
            token = create_access_token(identity= req_data.get('email'))
            print(token)

            return {"message":"Login successful",'status': HTTPStatus.OK}

        except Exception as e:
            return {'error': f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
blp.add_url_rule('/login', view_func=Login.as_view('Login'))

class Signup(MethodView):

    @blp.response(HTTPStatus.OK,schema=UserResponse(many=True))
    @jwt_required()
    def get(self):
        try:
            res = User.query.all()
            return res
        
        except Exception as e:
            return {'error': f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
    
    @blp.arguments(schema=SignupSchema())
    def post(self, req_data):
        try:
            hashed = bcrypt.hashpw(req_data.get('password').encode('utf-8'), salt)
            name = req_data.get('name').lower()
            
            entry = User(name=name, email=req_data.get('email'), password=hashed)
            db.session.add(entry)
            db.session.commit()
            return {"message":"User successfully registered.",'status': HTTPStatus.OK}
        except Exception as e:
            return {"error":f"{str(e)}",'status': HTTPStatus.INTERNAL_SERVER_ERROR}
    
    @blp.arguments(schema=UpdateSchema())
    @jwt_required()
    def put(self,req_data):
        try:
            res = User.query.filter_by(name=req_data.get('name')).first()
            product_type = req_data.get('product_type').lower()
            
            res.product_type = product_type
            db.session.commit()

            return {"message":"Product type successfully updated.",'status': HTTPStatus.OK}
        except Exception as e:
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
    @blp.arguments(schema=DeleteUserSchema())
    @jwt_required()
    def delete(self, get_data):
        try:
            res = User.query.filter_by(id=get_data.get('id')).first()
            
            db.session.delete(res)
            db.session.commit()

            return {"message":'User sucessfully deleted','status': HTTPStatus.OK}
        except Exception as e:
            return {'error':f'{str(e)}','status': HTTPStatus.INTERNAL_SERVER_ERROR}
        
        
blp.add_url_rule('/signup', view_func=Signup.as_view('SignUp'))

class ChangePassword(MethodView):

    @blp.arguments(schema=ChangePasswordSchema())
    @jwt_required()
    def put(self, req_data):
        try:
            email = get_jwt()['sub']
                
            email_exist = User.query.filter_by(email=email).first()

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
        
blp.add_url_rule('/changepassword', view_func=ChangePassword.as_view('ChangePassword'))

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

@blp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}