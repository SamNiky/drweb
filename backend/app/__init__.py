import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .settings import DB_LOGIN, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from .logger import init_logger

app = Flask(__name__, static_folder='../store', static_url_path='/')
app.app_context()
db = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_LOGIN}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

db.init_app(app)
migrate = Migrate(app, db)

init_logger('app')


from app.api import api
app.register_blueprint(api)