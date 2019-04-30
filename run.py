"""
   isort:skip_file
"""

import os

from dotenv import load_dotenv
from config import BASE_DIR

# Load env
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from flask_migrate import Migrate
from flask_migrate import upgrade as db_upgrade

from app import create_app, db

app = create_app(os.getenv('FLASK_ENV') or 'default')
app.app_context().push()
migrate = Migrate(app, db)


@app.cli.command()
def initdb():
    from app.models import User

    # Create admin user
    user = User.query.filter_by(username="admin").first()
    if not user:
        user = User(username="admin", password="admin")
        db.session.add(user)
        db.session.commit()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
