import pathlib

BASE_DIR = pathlib.Path(__file__).parent


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / "data" / "my_flask.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '83nifuse'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
    UPLOAD_FOLDER = 'upload'
    MAIL_SERVER = 'smtp.timeweb.ru'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = 'no-reply@greatwalk.ru'
    MAIL_PASSWORD = '83nifuse'
    MAIL_DEFAULT_SENDER = 'no-reply@greatwalk.ru'
    ADMINS = ['no-reply@greatwalk.ru']
    POSTS_PER_PAGE = 25
