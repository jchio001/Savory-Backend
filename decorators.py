from flask import jsonify, request
from functools import wraps
from jwt import DecodeError
from status_codes import HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_UNAUTHORIZED

import account_client
import savory_token_client
import time


# This is a collection of all annotations (known as decorators in Python land) that will intercept an endpoint before
# executing the endpoint's core logic.

# This decorator validates a request's token. Validations include:
# - Is there actually a token attached to the request?
# - Is the token one that's encoded by us?
# - Does the token belong to a user in our database?
# - Has the token expired?
# If the token has gone through all four of these checks, an Account object will be magic'd into your endpoint for you
# to consume with <insert generic CRUD business logic>
def ValidateToken(token_location):
    def validate_token_wrapper(f):
        @wraps(f)
        def validate_token(*args, **kwargs):

            encoded_savory_token = request.headers.get('Authorization') if token_location == 'header' \
                else request.args.get('token')

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

    return validate_token_wrapper
