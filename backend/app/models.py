from . import db


# Модель для журнала файлов
class FilesRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    dir_name = db.Column(db.String)
    content_type = db.Column(db.String)
    format_type = db.Column(db.String)
    date_stamp = db.Column(db.DateTime)