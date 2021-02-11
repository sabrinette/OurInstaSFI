from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key="123456"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:@127.0.0.1:3306/ourinsta"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.create_all()
db.session.commit()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from OurInsta import routes
