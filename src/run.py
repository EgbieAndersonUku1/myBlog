from flask_script import Manager, Server
from app import create_app

manager = Manager(create_app)
manager.add_command('runserver', Server(
    use_reloader=True,
    use_debugger=True
))



@manager.shell
def create_shell():
      return dict(app=create_app)

if  __name__ == '__main__':
    manager.run() # start the flask web server by running the command: 'python run.py runserver' in the command line
                              # url link: http://127.0.0.1:5000/<some url page >

