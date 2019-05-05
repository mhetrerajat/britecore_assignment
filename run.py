"""
   isort:skip_file
"""

import os
import click

from dotenv import load_dotenv
from config import BASE_DIR

# Load env
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from flask_migrate import Migrate

from app import create_app, db
from app.utils.parser import DataParser

application = create_app(os.getenv('FLASK_ENV') or 'default')
application.app_context().push()
migrate = Migrate(application, db)


@application.cli.command()
def initdb():
    """
        Initialize the database with admin user
    """
    from app.models import User

    # Create admin user
    user = User.query.filter_by(username="admin").first()
    if not user:
        user = User(username="admin", password="admin")
        db.session.add(user)
        db.session.commit()


@application.cli.command(name="import")
@click.argument("path")
def import_data(path):
    """
        Imports data from csv file
    """
    p = DataParser(path)
    p.parse()


if __name__ == "__main__":
    application.run(host='0.0.0.0')
