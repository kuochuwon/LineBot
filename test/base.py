import os

from unittest import TestCase
from app.main import db
from app.main.model.user import sdUser
# from app.main.model.task import sdTask
# from app.main.model.bible import Bible
from manage import app

file_dir = os.path.dirname(__file__)


class BaseTestCase(TestCase):
    """ Base Tests """

    # HINT the data will be used from func:test_check_line_user
    def add_users(self):
        for i in range(3):
            obj = sdUser.add(f"test_{i}", f"0xabb123{i}")
            db.session.add(obj)
        db.session.commit()

    def create_app(self):
        app.config.from_object("app.main.config.TestingConfig")
        return app

    def setUp(self):
        self.create_app()
        db.create_all()
        db.session.commit()
        self.add_users()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BaseTestCase2(TestCase):
    """ Without initial db """

    def create_app(self):
        app.config.from_object("app.main.config.TestingConfig")
        return app

    def setUp(self):
        self.create_app()
