from functools import wraps

import savory_token_client
import time


class ExpiredTokenException(Exception):
    pass


# TODO(jchiou): I'm pretty sure I can pass in the user id into kwargs
def ValidateToken(f):
    @wraps(f)
    def validate_token(*args, **kwargs):
        from flask import request
        decoded_token = savory_token_client.decode_savory_token(request.headers.get('Authorization'))

        now = int(time.time())

        if decoded_token.get('expires_at') < now:
            raise ExpiredTokenException()

        return f(*args, **kwargs)

    return validate_token
