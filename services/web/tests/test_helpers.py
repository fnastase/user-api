import unittest 
from flask import current_app, Flask

from app import helpers
from app import app, db


class HelpersTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_is_valid_email(self):
        self.assertTrue(helpers.is_valid_email('name@email.com'))
        self.assertFalse(helpers.is_valid_email('123456'))

    def test_is_valid_activation_code(self):
        self.assertTrue(helpers.is_valid_activation_code('1234'))
        self.assertFalse(helpers.is_valid_activation_code('qwerty'))

    def test_is_valid_uuid(self):
        self.assertTrue(helpers.is_valid_uuid('7ee13bdb-533a-4822-af81-1d09e3e5800b'))
        self.assertFalse(helpers.is_valid_uuid('qwerty'))

    def test_generate_activation_code(self):
        activation_code = helpers.generate_activation_code()
        self.assertTrue(helpers.is_valid_activation_code(activation_code))

    def test_encode_activation_data(self):
        uuid = '7ee13bdb-533a-4822-af81-1d09e3e5800b'
        code = '6389'
        activation_data = helpers.encode_activation_data(uuid, code)
        self.assertEquals(activation_data, 'N2VlMTNiZGItNTMzYS00ODIyLWFmODEtMWQwOWUzZTU4MDBiOjYzODk=')

    def test_decode_activation_data_uuid(self):
        activation_data = 'N2VlMTNiZGItNTMzYS00ODIyLWFmODEtMWQwOWUzZTU4MDBiOjYzODk='
        uuid = helpers.decode_activation_data_uuid(activation_data)
        self.assertEquals(uuid, '7ee13bdb-533a-4822-af81-1d09e3e5800b')

    def decode_activation_data_code(self):
        activation_data = 'N2VlMTNiZGItNTMzYS00ODIyLWFmODEtMWQwOWUzZTU4MDBiOjYzODk='
        code = helpers.decode_activation_data_uuid(activation_data)
        self.assertEquals(code, '6389')
