import unittest
from flask import current_app, Flask, url_for
from flask_sqlalchemy import model

from datetime import datetime, timedelta

from app import models, helpers
from app import app, db


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        db.create_all()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_create_user(self):
        with app.test_client() as test_client:
            response = test_client.post('/users', json={"email": "user11@email.com", "password": "password"})
            assert response.status_code == 200
            assert b"User added" in response.data

    def test_activate_user_ok(self):
        with app.test_client() as test_client:
            response = test_client.post('/users', json={"email": "user12@email.com", "password": "password"})
            assert response.status_code == 200
            assert b"User added" in response.data

        user = models.get_user_by_email("user12@email.com")
        activation_string = helpers.encode_activation_data(user.uuid, user.activation_code)

        with app.test_client() as test_client:
            response = test_client.get('/activate/' + activation_string)
            assert response.status_code == 200
            assert b"User activated" in response.data

    def test_user_already_activated(self):
        user = models.get_user_by_email("user12@email.com")
        activation_string = helpers.encode_activation_data(user.uuid, user.activation_code)

        with app.test_client() as test_client:
            response = test_client.get('/activate/' + activation_string)
            assert response.status_code == 400

    def test_activate_user_expired(self):
        with app.test_client() as test_client:
            response = test_client.post('/users', json={"email": "user13@email.com", "password": "password"})
            assert response.status_code == 200
            assert b"User added" in response.data

        user = models.get_user_by_email("user13@email.com")
        user.activation_email_date = user.activation_email_date - timedelta(days=1)

        db.session.commit()

        activation_string = helpers.encode_activation_data(user.uuid, user.activation_code)

        with app.test_client() as test_client:
            response = test_client.get('/activate/' + activation_string)
            assert response.status_code == 400
            assert b"expired" in response.data
