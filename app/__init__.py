from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import psycopg2


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

conn = psycopg2.connect(dbname=app.config["DB_NAME"], user=app.config["DB_USER"],
                        password=app.config["DB_PASS"], host=app.config["DB_HOST"])
cursor = conn.cursor()

from app import routes, models

# To create tables in Heroku PostgreSQL execute in Python Console:
#from app import db
#db.create_all()