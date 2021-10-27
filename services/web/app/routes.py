from app import helpers
from flask import json, request, Response, jsonify
import logging
import datetime
from werkzeug.exceptions import BadRequest, NotFound
from app import app, models
from app.models import User
from app.email import EmailAPIController


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    return_list = []

    for user in users:
        user_entry = {
            'email': user.email,
            'id': user.id,
            'password_hash': user.password_hash,
            'activation_email_date': user.activation_email_date,
            'activation_code': user.activation_code
        }
        return_list.append(user_entry)

    return jsonify(return_list)


@app.route('/users', methods=['POST'])
def create_user():
    '''User registration endpoint'''

    request_data = request.get_json()

    email = request_data['email']
    password = request_data['password']

    # validate input data
    if not helpers.is_valid_email(email):
        logging.error("Invalid email")
        raise BadRequest("Invalid email")

    if not helpers.is_password_complex(password):
        logging.error("Invalid password complexity")
        raise BadRequest("Invalid password complexity")


    # check registered
    user = models.get_user_by_email(email)

    if user:
        logging.error("User already registered")
        raise BadRequest("User already registered")



    # generate activation code
    activation_code = helpers.generate_activation_code()

    logging.info(f"activation_code: {activation_code}")


    # create user object
    user = models.insert_user(email, password)
    logging.info(f"user inserted: {user}")
    print(user)

    # update user activation code
    models.set_activation_code(user, activation_code)

    # send email
    email_controller = EmailAPIController("external.mail.api")

    email_controller.send_email_request(user)

    # save to DB
    models.set_activation_email_date(user)

    response = jsonify({'message': 'User added', 'result': user.email})

    return response


@app.route('/activate/<activation_data>', methods=['GET'])
def activate(activation_data: str):
    '''User activation endpoint'''

    # Decode uuid from the activation data
    decoded_uuid = ''
    try:
        decoded_uuid = helpers.decode_activation_data_uuid(activation_data)
    except Exception as ex:
        logging.error("Invalid activation data", str(ex))
        raise BadRequest("Invalid activation data")

    if not helpers.is_valid_uuid(decoded_uuid):
        logging.error("Invalid uuid in the activation data")
        raise BadRequest("Invalid uuid in the activation data")

    # Decode activation code from the activation data
    decoded_activation_code = ''
    try:
        decoded_activation_code = helpers.decode_activation_data_code(activation_data)
    except Exception as ex:
        logging.error("Invalid activation data", str(ex))
        raise BadRequest("Invalid activation data")

    if not helpers.is_valid_activation_code(decoded_activation_code):
        logging.error("Invalid code in the activation data")
        raise BadRequest("Invalid code in the activation data")

    # get user from DB
    user = models.get_user_by_uuid(decoded_uuid)

    if user is None:
        logging.error("User uuid not found")
        raise BadRequest("User uuid not found")

    # check user already activated
    if user.is_active:
        raise BadRequest("User already activated")

    if not user:
        logging.error("Decoded email or user not found")
        raise BadRequest("Decoded email or not found")

    # check activation code
    if user.activation_code != decoded_activation_code:
        raise BadRequest("Activation code is different")

    # check expired code
    time_delta = datetime.datetime.utcnow() - user.activation_email_date
    print(f'time_delta.total_seconds() = {time_delta.total_seconds()}')
    if time_delta.total_seconds() > 60:
        raise BadRequest("Activation code is expired")

    # activate user
    models.update_user_activated(user)

    response = jsonify({'message': 'User activated', 'result': user.email})

    return response
