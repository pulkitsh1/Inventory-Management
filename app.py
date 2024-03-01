from flask import Flask
from http import HTTPStatus
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from src.modules.user.endpoints import blp as user_blp
from src.modules.inventory.endpoints import blp as stock_blp
from src.modules.transactions.endpoints import blp as transaction_blp
from src.modules.product_type.endpoints import blp as type_blp
from src.modules.employees.endpoints import blp as emp_blp
from src.modules.assigned.endpoints import blp as assign_blp
from src.modules.user.blocklist import BlockList
from src.service_modules.db.conn import db
import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQL_CONNECTION
app.config['JWT_SECRET_KEY'] = config.JWT_KEY

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

app.register_blueprint(user_blp)
app.register_blueprint(stock_blp)
app.register_blueprint(transaction_blp)
app.register_blueprint(type_blp)
app.register_blueprint(emp_blp)
app.register_blueprint(assign_blp)

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
    