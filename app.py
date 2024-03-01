from flask import Flask
from http import HTTPStatus
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from src.modules.user.endpoints import api as user_api
from src.modules.inventory.endpoints import api as stock_api
from src.modules.transactions.endpoints import api as transaction_api
from src.modules.product_type.endpoints import api as type_api
from src.modules.employees.endpoints import api as emp_api
from src.modules.assigned.endpoints import api as assign_api
from src.modules.user.blocklist import BlockList
from src.service_modules.db.conn import db
import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQL_CONNECTION
app.config['JWT_SECRET_KEY'] = config.JWT_KEY

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

app.register_blueprint(user_api)
app.register_blueprint(stock_api)
app.register_blueprint(transaction_api)
app.register_blueprint(type_api)
app.register_blueprint(emp_api)
app.register_blueprint(assign_api)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BlockList

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return(
        {
            "description": "User has been logged out",
            "error": "token_revoked"
        },
        HTTPStatus.UNAUTHORIZED
    )


if __name__ == '__main__':
    # upgrade()
    app.run(debug=True)
    