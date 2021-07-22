from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin



app = Flask(__name__)
app.config['SECRET_KEY'] = 'a5c5cbdf1428d6fe3f40a3114eea2ac4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

from OnlineExamSystem.models import Question , User ,MyModelView , Subjects

admin = Admin(app)
admin.add_view(MyModelView(User , db.session))
admin.add_view(MyModelView(Question , db.session))
admin.add_view(MyModelView(Subjects , db.session))
from OnlineExamSystem import routes


