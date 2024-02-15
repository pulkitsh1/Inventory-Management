import os
from dotenv import load_dotenv

load_dotenv()

SQL_CONNECTION = os.getenv('connection_string')
JWT_KEY = os.getenv('jwt_key')