
"""API для работы с файлами"""

import os
import logging
import hashlib
from datetime import datetime

from flask import Blueprint, request, send_from_directory

from .models import *

# Создаем эскиз и инициализируем логирование для сервиса app.api
api = Blueprint('api', __name__)
log = logging.getLogger('app.api')

# Переменые с путями для файлов
UPLOAD_FOLDER = os.path.dirname(__file__).replace('/app', '/store')
RAW_DIRECTORY = f'{UPLOAD_FOLDER}/raw'


# API для загрузки файлов
@api.route('/api/v1/file/upload', methods=['POST'])
def upload_file():

    # Проверяем на form-data
    if request.files:

        # Обработка файла по ключу
        try:
            upload_file = request.files['file']
        except:
            message = 'key error: The key "file" is not found'
            log.error(message)
            return {'error': message}, 400

        # Сохраняем тип и расширение файла
        content_type = upload_file.content_type.split('/')

        # Сохраняем "сырой" файл в специальную директорию
        try:
            upload_file.save(os.path.join(RAW_DIRECTORY, f'raw.{content_type[1]}'))
        except:
            message = f'Error with save new file'
            log.error(message)
            return {'error': message}, 500

        # Хэшируем файл
        try:
            with open(f'{RAW_DIRECTORY}/raw.{content_type[1]}', 'rb') as file:
                md5Hash = hashlib.md5(file.read())
        except:
            message = 'Error with hashing file'
            log.error(message)
            return {'error': message}, 500

        # Получаем новое имя и директорию для файла
        filename = md5Hash.hexdigest()
        directory = f'{UPLOAD_FOLDER}/{filename[:2]}'

        # Проверяем существует ли файл
        check_file = FilesRegister.query.filter_by(name=filename).first()
        if check_file is not None:
            message = f'This file with filename: {filename} already exists'
            log.info(message)
            return {'error': message}, 400

        # Создаем директорию если ее не существует
        if not os.path.isdir(directory):
            log.info(f'Create new directory: {directory}')
            os.makedirs(directory)

        # Переносим и переименовываем файл
        os.replace(f'{RAW_DIRECTORY}/raw.{content_type[1]}', f'{directory}/raw.{content_type[1]}')
        os.rename(f'{directory}/raw.{content_type[1]}', f'{directory}/{filename}.{content_type[1]}')
        log.info(f'File with filename {filename} has been saved')

        # Делаем запись в журнал файлов в БД
        try:
            new_entry_in_register = FilesRegister(name=filename, dir_name=directory, date_stamp=datetime.now(),
                                                  content_type=content_type[0], format_type=content_type[1])
            db.session.add(new_entry_in_register)
            db.session.commit()
        except:
            message = 'New entry in register hasnt been save'
            log.error(message)
            return {'error': message}, 500

        log.info('New entry in register has been save')

        # Возвращаем название файла
        return {'filename': filename}, 200

    # Если запрос не содержит файл
    else:
        message = 'POST request support only form-data with uploaded file'
        log.error(message)
        return {'error': message}, 400


# API для скачивания файла
@api.route('/api/v1/file/download/<filename>', methods=['GET'])
def download_file(filename):

    # Находим файл в журнале
    file = FilesRegister.query.filter_by(name=filename).first()

    # Если файл найден в журнале отдаем его клиенту, или отправляем ошибку
    if file is not None:
        log.info(f'File {file.name}.{file.format_type} get ready for download')
        return send_from_directory(file.dir_name, f'{file.name}.{file.format_type}', as_attachment=True), 200
    else:
        message = f'File with filename: {filename} not found'
        log.info(message)
        return {'error': message}, 400


# API для удаления файлов
@api.route('/api/v1/file/delete/<filename>', methods=['GET'])
def delete_file(filename):

    # Находим файл в журнале
    file = FilesRegister.query.filter_by(name=filename).first()

    # Если файл найден в журнале, то удаляем его, или отправляем ошибку
    if file is not None:

        # Удаляем файл
        try:
            os.remove(f'{file.dir_name}/{file.name}.{file.format_type}')
        except:
            message = f'File {file.name}.{file.format_type} cant removed'
            log.error(message)
            return {'error': message}, 500

        # Проверяем директорию на пустоту и удаляем если пустая
        if not os.listdir(file.dir_name):
            try:
                os.rmdir(file.dir_name)
            except:
                message = f'Directory {file.dir_name} cant removed'
                log.error(message)

        # Удаляем запись о файле в журнале
        try:
            db.session.delete(file)
            db.session.commit()
        except:
            message = f'Error with delete entry in FilesRegister with ID: {file.id}'
            log.error(message)

        # Отправляем ответ
        message = f'File with filename {filename}, is deleted'
        log.info(message)
        return {'message': message}, 200

    else:
        message = f'File with filename: {filename} not found'
        log.info(message)
        return {'error': message}, 400