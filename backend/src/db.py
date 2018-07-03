import psycopg2
import os
from flask_sqlalchemy import SQLAlchemy


class DB():
    def __init__(self, app):
        user = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]

        try:
            self.conn = psycopg2.connect(f"dbname='kickerscore' user='{user}' host='kickerscore-db-service.kickerscore.svc.cluster.local' password='{password}'")
        except Exception as e:
            raise e
