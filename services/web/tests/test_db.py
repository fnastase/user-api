import unittest
from flask import current_app, Flask

from app import models
from app import app, db


class DbTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        db.create_all()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_user_set_and_check_password(self):
        user = models.User()
        user.set_password('password')
        self.assertNotEquals(user.password_hash, 'password')
        self.assertTrue(user.check_password('password'))

    def test_insert_user(self):
        user = models.insert_user('user1@email.com', 'password')
        self.assertNotEquals(user.id, None)

    def test_is_registered(self):
        user = models.insert_user('user2@email.com', 'password')
        self.assertTrue(models.is_registered('user2@email.com'))

    def test_get_user_by_email(self):
        user = models.insert_user('user3@email.com', 'password')
        fetched_user = models.get_user_by_email('user3@email.com')
        self.assertEquals(fetched_user, user)

    def test_get_user_by_uuid(self):
        user = models.insert_user('user4@email.com', 'password')
        fetched_user = models.get_user_by_uuid(user.uuid)
        self.assertEquals(fetched_user, user)

    def test_update_user_activated(self):
        user = models.insert_user('user5@email.com', 'password')
        user = models.update_user_activated(user)
        self.assertTrue(user.is_active)

    def test_set_activation_email_date(self):
        user = models.insert_user('user6@email.com', 'password')
        user = models.set_activation_email_date(user)
        self.assertIsNotNone(user.activation_email_date)

    def test_set_activation_code(self):
        user = models.insert_user('user7@email.com', 'password')
        user = models.set_activation_code(user, '1234')

        user = models.get_user_by_email('user7@email.com')
        self.assertEquals(user.activation_code, '1234')