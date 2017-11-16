import unittest

from app import create_app, db
from app.api.models import User

import coverage

from flask_migrate import MigrateCommand

from flask_script import Manager

COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'app/tests/*'
    ]
)

COV.start()

app = create_app()
manager = Manager(app)


manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('app/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('app/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def seed_db():
    """Seeds the database."""
    db.session.add(User(username='jamie', email="jamie@test.com", password="password"))
    db.session.add(User(username='jamieconnelly', email="jamieconnelly@test.org", password="password"))
    db.session.commit()


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
