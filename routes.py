import json
import logging
import account_client
import photo_client

from decorators import ValidateFacebookToken, ValidateToken
from flask import Flask, request
from models import Photo
from status_codes import HTTP_STATUS_OK

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/connect', methods=['GET'])
@ValidateFacebookToken
def connect_with_social_platform(*args, **kwargs):
    response_dict, status_code = account_client.create_or_update_existing_account(kwargs.get('facebook_account'))
    return json.dumps(response_dict), status_code


@app.route('/account/me')
@ValidateToken
def get_my_profile(*args, **kwargs):
    response_dict, status_code = account_client.get_account_info(kwargs.get('account'))
    return json.dumps(response_dict), status_code


@app.route('/account/me/photos', methods=['GET'])
@ValidateToken
def get_my_photos(*args, **kwargs):
    photos_page = photo_client.get_stubbed_photos(kwargs.get('account'), request.args.get('last_id'))
    return json.dumps(list(map(Photo.to_dict, photos_page))), HTTP_STATUS_OK


@app.route('/photo', methods=['POST'])
@ValidateToken
def post_photo(*args, **kwargs):
    response_dict, status_code = photo_client.post_photo(kwargs.get('account'), request)
    return json.dumps(response_dict), status_code


@app.route('/following/photos', methods=['GET'])
@ValidateToken
def get_photos_for_feed(*args, **kwargs):
    response_dict, status_code = photo_client.get_photos_for_feed(kwargs.get('account'), request.args.get('last_id'))
    return json.dumps(response_dict), status_code


# Since everything that we return will literally be a json, might as well use @app.after_request
# instead of attaching a custom annotation (aka decorators in Python land)
@app.after_request
def set_content_type(response):
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    app.run()
