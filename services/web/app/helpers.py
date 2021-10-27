import re
import random
import base64
from uuid import UUID, uuid4


def is_valid_email(email: str) -> bool:
    '''Returns true if the email string is a valid email address'''

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(re.fullmatch(regex, email)):
        return True
    else:
        return False


def is_valid_activation_code(activation_code: str) -> bool:
    '''Returns true if the activation_code string is a valid (4 digits)'''

    regex = r'[0-9]{4}$'

    if(re.fullmatch(regex, activation_code)):
        return True
    else:
        return False


def is_valid_uuid(uuid: str) -> bool:
    '''Returns true if uuid string is a valid UUID'''
    try:
        uuid_obj = UUID(uuid, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid


def generate_activation_code() -> str:
    '''Generates a 4 digits random activation code'''

    activation_code = str(random.randint(0, 9)) + str(random.randint(0, 9)) \
        + str(random.randint(0, 9)) + str(random.randint(0, 9))
    return activation_code


def encode_activation_data(uuid: str, activation_code: str) -> str:
    '''Encodes input data (email and activation code concatenated as "uuid:code") into a base64 string'''
    activation_data = uuid + ':' + activation_code
    activation_data_bytes = activation_data.encode('ascii')
    base64_bytes = base64.b64encode(activation_data_bytes)
    base64_string = base64_bytes.decode('ascii')
    return base64_string


def decode_activation_data_uuid(base64_string: str) -> str:
    '''Decodes email from a besa64 encoded activation data string'''
    base64_bytes = base64_string.encode('ascii')
    activation_data_bytes = base64.b64decode(base64_bytes)
    activation_data = activation_data_bytes.decode('ascii')
    activation_data_parts = activation_data.split(':')
    uuid = activation_data_parts[0]
    return uuid


def decode_activation_data_code(base64_string: str) -> str:
    '''Decodes activation code from a besa64 encoded activation data string'''
    base64_bytes = base64_string.encode('ascii')
    activation_data_bytes = base64.b64decode(base64_bytes)
    activation_data = activation_data_bytes.decode('ascii')
    activation_data_parts = activation_data.split(':')
    code = activation_data_parts[1]
    return code


def is_password_complex(password: str) -> bool:
    '''Checks if password is complex'''

    # TODO insert the password complexity check (with regex)

    if len(password) < 8:
        return False

    return True
