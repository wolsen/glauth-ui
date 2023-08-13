from flask_bootstrap import Bootstrap4
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

bootstrap = Bootstrap4()
db = SQLAlchemy()
login = LoginManager()
mail = Mail()
migrate = Migrate()
