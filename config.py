import ssl
# config
import os

hostname = os.environ.get('DB_HOSTNAME')
port = os.environ.get('DB_PORT')
username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
database = os.environ.get('DB_DATABASE')

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(username, password, hostname, port, database)
SQLALCHEMY_DATABASE_URI = DB_URI

MAIL_SERVER = 'smtp.mail.yahoo.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'wilson860731@yahoo.com.tw'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = 'wilson860731@yahoo.com.tw'

SECRET_KEY = 'a;sdjf;asjdf;lkjsad;ljawergpj'