from app import create_app, db
from flask_script import Manager

app = create_app()
manager = Manager(app)


@manager.command
def db_init():
    db.create_all()

if __name__ == "__main__":
    manager.run()
