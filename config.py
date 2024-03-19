import redis
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME",'inventory')

jwt_redis_blocklist = redis.StrictRedis(
    host=DB_HOST, port=6379, db=0, decode_responses=True
)
ACCESS_EXPIRES = timedelta(hours=1)
SQL_CONNECTION = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
JWT_KEY = os.getenv('JWT_KEY', '298688260635158597817274397161605765004')
