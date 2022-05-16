import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'mbapp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    POSTS_PER_PAGE = 3  # nums posts on a page
    LANGUAGES = ['en', 'ru', 'ua']  # for flask_babel
    # add mail  support
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@example.com']

    # for search
    MSEARCH_INDEX_NAME = 'msearch'
    MSEARCH_BACKEND = 'whoosh'  # simple,whoosh,elaticsearch, default is simple
    MSEARCH_PRIMARY_KEY = 'id'
    MSEARCH_ENABLE = True    # auto create or update index
    # MSEARCH_LOGGER = logging.DEBUG    # logger level, default is logging.WARNING
    SQLALCHEMY_TRACK_MODIFICATIONS = True    # SQLALCHEMY_TRACK_MODIFICATIONS must be set to True when msearch auto index is enabled

