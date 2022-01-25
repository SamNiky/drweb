
""" Файл инициализации и запуска всего приложения """

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .settings import DB_LOGIN, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from .logger import init_logger

# Инициализируем приложение, устанавливаем CLI отслеживание и создаем экземпляр ORM для работы с БД
app = Flask(__name__, static_folder='../store', static_url_path='/')
app.app_context()
db = SQLAlchemy()

# Настройки конфигурации приложения
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_LOGIN}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Инициализируем БД, Менеджер миграций, Менеджер логирования
db.init_app(app)
migrate = Migrate(app, db)
init_logger('app')


# Инициализируем эскиз app.api
from app.api import api
app.register_blueprint(api)