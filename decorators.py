from facebook_client import FacebookException
from flask import jsonify, request, Response
from functools import wraps
from jwt import DecodeError
from status_codes import HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_UNAUTHORIZED

import user_client
import facebook_client
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

        user = user_client.get_user(decoded_token.get('id'))

        if not user:
            response = jsonify({'error': 'User id does not exist in the system.'})
            response.status_code = HTTP_STATUS_BAD_REQUEST
            return response

        now = int(time.time())
        if decoded_token.get('expires_at') < now:
            response = jsonify({'error': 'Expired token.'})
            response.status_code = HTTP_STATUS_UNAUTHORIZED
            return response

        return f(*args, **kwargs, user=user)

    return validate_token


# Given a user id in a URI path, validates where or not the user is a valid user/exists in our database.
def ValidateUserId(f):
    @wraps(f)
    def validate_user(*args, **kwargs):
        try:
            if 'user_id' in kwargs:
                user_id = int(kwargs.get('user_id'))
            else:
                response = jsonify({'error': 'user_id not present in path.'})
                response.status_code = HTTP_STATUS_BAD_REQUEST
                return response
        except ValueError:
            response = jsonify({'error': 'Invalid user id.'})
            response.status_code = HTTP_STATUS_BAD_REQUEST
            return response

        user = user_client.get_user(user_id)

        if not user:
            response = jsonify({'error': 'User id does not exist in the system.'})
            response.status_code = HTTP_STATUS_BAD_REQUEST
            return response

        return f(*args, **kwargs, user_in_uri=user)

    return validate_user


# This decorator converts a token from Facebook into a FacebookAccount object and passes that object into the endpoint
# method.
def ValidateFacebookToken(f):
    @wraps(f)
    def validate_facebook_token(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            response = jsonify({'error': 'Missing Facebook token'})
            response.status_code = HTTP_STATUS_BAD_REQUEST
            return response

        try:
            facebook_account = facebook_client.get_profile(request.args.get('token'))
            return f(*args, **kwargs, facebook_account=facebook_account)
        except FacebookException as e:
            response = Response(e.error_body)
            response.status_code = e.status_code
            return response

    return validate_facebook_token
