# Used to create a database object for the application
# 為了解決循環引用的問題

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()