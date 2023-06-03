import os

from starlette.config import Config

config = Config('.env')

DB = 'postgresql'
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'db_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'db_password')
DB_NAME = os.getenv('DB_NAME', 'verifier-db')
DB_PORT = os.getenv('DB_PORT', '5431')

DATABASE_URL = f"{DB}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

