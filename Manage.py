import os
from webapp import create_app
from flask_script import Manager, Server, Shell

app = create_app("development")
manager = Manager(app)
port = os.getenv('PORT', '8081')
manager.add_command("runserver", Server(host="0.0.0.0", port=int(port)))


if __name__ == '__main__':
    manager.run()