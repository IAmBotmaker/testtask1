import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import psycopg2
import redis


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

conn = psycopg2.connect(dbname=app.config["DB_NAME"], user=app.config["DB_USER"],
                        password=app.config["DB_PASS"], host=app.config["DB_HOST"])
cursor = conn.cursor()

from app import routes, models, tasks

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

# To create tables in Heroku PostgreSQL execute in Python Console:
#from app import db
#db.create_all()
