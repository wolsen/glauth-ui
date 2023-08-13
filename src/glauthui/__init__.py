from flask import Flask
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from glauthui.config import Config
from secrets import token_urlsafe

from glauthui.extensions import bootstrap
from glauthui.extensions import db
from glauthui.extensions import login
from glauthui.extensions import mail
from glauthui.extensions import migrate

import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from glauthui import models
        # Note: hack to resolve invalid backref pgroups
        models.User()

        from glauthui.views import routes  # noqa
        from glauthui.views import adminview  # noqa
        from glauthui import utils  # noqa

    migrate.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    login.login_view = 'login'
    mail.init_app(app)
    bootstrap.init_app(app)

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['MAIL_ADMIN'], subject='{} - Failure'.format(app.config['APPNAME']),
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        # Only log to file if configure in UI?
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/glauth_ui.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Glauth UI')

        if app.config['SECRET_KEY'] == 'you-will-never-guess':
            app.logger.warning('No unique SECRET_KEY set to secure the application.\n \
                                You can the following randomly generated key:\n \
                                {}'.format(token_urlsafe(50)))
            exit()

    return app


def run_server():
    app = create_app()
    app.run()


if __name__ == "__main__":
    run_server()
