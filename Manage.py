import os

from webapp import create_app
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from webapp.models import db

app = create_app("development")
manager = Manager(app)
migrate = Migrate(app, db)

port = os.getenv('PORT', '8081')
manager.add_command("runserver", Server(host="0.0.0.0", port=int(port)))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    db.create_all()
    manager.run()