import json
import logging
import account_client
import photo_client

from decorators import ValidateToken
from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/connect', methods=['GET'])
def connect_with_social_platform():
    return json.dumps(account_client.create_or_update_existing_profile(request.args.get('token')))


@app.route('/photo', methods=['POST'])
@ValidateToken
def post_photo():
    return json.dumps(photo_client.post_photo(request))


# Since everything that we return will literally be a json, might as well use @app.after_request
# instead of attaching a custom annotation (aka decorators in Python land)
@app.after_request
def set_content_type(response):
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    app.run()
