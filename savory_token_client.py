import jwt
import os
import time

jwt_secret = os.environ['SAVORY_JWT_SECRET']

# For now, let's make the token expire after 1 month. Granted this does literally nothing at the moment.
def create_savory_token(account):
    token_expiration = int(time.time()) + 2592000
    return jwt.encode({'id': account.id, 'expires_at': token_expiration}, jwt_secret, algorithm='HS512')
