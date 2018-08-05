from flask import jsonify, request
from functools import wraps
from jwt import DecodeError
from status_codes import HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_UNAUTHORIZED

import account_client
import logging
import savory_token_client
import time


def ValidateToken(f):
    @wraps(f)
    def validate_token(*args, **kwargs):
        encoded_savory_token = request.headers.get('Authorization')
        if not encoded_savory_token:
            response = jsonify({'error': 'Missing token'})
            response.status_code = HTTP_STATUS_BAD_REQUEST
            return response

        try:
            decoded_token = savory_token_client.decode_savory_token(encoded_savory_token)
        except DecodeError:
            response = jsonify({'error': 'Invalid token.'})
            response.status_code = HTTP_STATUS_BAD_REQUEST
            return response

        account = account_client.get_account(decoded_token.get('id'))

        if not account:
            response = jsonify({'error': 'Account id does not exist in the system.'})
            response.status_code = HTTP_STATUS_BAD_REQUEST
            return response

        now = int(time.time())
        if decoded_token.get('expires_at') < now:
            response = jsonify({'error': 'Expired token.'})
            response.status_code = HTTP_STATUS_UNAUTHORIZED
            return response

        return f(*args, account=account, **kwargs)

    return validate_token
