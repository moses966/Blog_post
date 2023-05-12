import os
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate

# Creating a flask application instance
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# setting up the migration framework to work with the application and the database
migrate = Migrate(app, db)

# decorator to generate the shell context
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)