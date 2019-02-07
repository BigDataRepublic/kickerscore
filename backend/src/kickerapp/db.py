import os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_HOST = os.environ["POSTGRES_HOST"]
DB_DATABASE = "kickerscore"
