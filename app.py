from flask import Flask
from http import HTTPStatus
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from src.modules import user_api, stock_api, transaction_api, type_api, emp_api, assign_api
from src.service_modules.db.conn import db
import config
from src.utils.helper import UPLOAD_FOLDER
from flask_smorest import Api
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQL_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['JWT_SECRET_KEY'] = config.JWT_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.ACCESS_EXPIRES
app.config['PROPAGATE_EXCEPTION'] = True
app.config['API_TITLE'] = "Inventory Management API's"
app.config['API_VERSION'] = "v1"
app.config['OPENAPI_VERSION'] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = "/"
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger"
app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
api = Api(app)

blplist = [user_api, stock_api, transaction_api, type_api, emp_api, assign_api]
for blp in blplist:
    api.register_blueprint(blp)
    
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = config.jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return(
        {
            "description": "User has been logged out",
            "error": "token_revoked"
        },
        HTTPStatus.UNAUTHORIZED
    )

def run_migrations():
    with app.app_context():
        os.system("flask db upgrade")

if __name__ == '__main__':
    run_migrations()
    app.run(host='0.0.0.0', port=5000, debug=True)
    