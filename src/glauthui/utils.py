from flask import current_app as app
from glauthui import models
import click
import hashlib


# Security - Generate GLAUTH compatible password hashs
def generate_password_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def check_password_hash(the_hash, password):
    if the_hash != hashlib.sha256(password.encode('utf-8')).hexdigest():
        return False
    return True


@app.cli.command()
def createdbdata():
    """Creating example db"""
    if models.User.query.count() == 0:
        app.logger.info('No Data in DB, creating example dataset')
        click.echo('Creating Example DB')
        models.create_basic_db()
    else:
        app.logger.info('Data in DB already exists.')
