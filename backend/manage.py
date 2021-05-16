import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

# https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/

env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()