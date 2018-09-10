import json
import logging
import photo_client
import savory_token_client
import user_client

from decorators import ValidateFacebookToken, ValidateToken, ValidateUserId
from flask import Flask, request
from models import Photo
from status_codes import HTTP_STATUS_OK

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/connect', methods=['GET'])
@ValidateFacebookToken
def connect_with_social_platform(*args, **kwargs):
    response_dict, status_code = user_client.create_or_update_existing_account(kwargs.get('facebook_account'))
    return json.dumps(response_dict), status_code


@app.route('/token', methods=['GET'])
@ValidateToken
def exchange_token(*args, **kwargs):
    response_dict = {'token': savory_token_client.create_savory_token(kwargs.get('user'))}
    return json.dumps(response_dict), HTTP_STATUS_OK


@app.route('/user/me', methods=['GET'])
@ValidateToken
def get_my_profile(*args, **kwargs):
    response_dict, status_code = user_client.get_user_info(kwargs.get('user'))
    return json.dumps(response_dict), status_code


@app.route('/user/me/following', methods=['GET'])
@ValidateToken
def get_users_being_followed_by_me(*args, **kwargs):
    followed_users_dict_list, status_code = user_client.get_followed_users_for_user(kwargs.get('user'))
    return json.dumps(followed_users_dict_list), status_code


@app.route('/user/<user_id>/follow', methods=['POST'])
@ValidateToken
@ValidateUserId
def follow_user(*args, **kwargs):
    response_dict, status_code = user_client.follow_user(kwargs.get('user'),
                                                         kwargs.get('user_in_uri'))
    return json.dumps(response_dict), status_code


@app.route('/user/<user_id>/unfollow', methods=['POST'])
@ValidateToken
@ValidateUserId
def unfollow_user(*args, **kwargs):
    response_dict, status_code = user_client.unfollow_user(kwargs.get('user'),
                                                           kwargs.get('user_in_uri'))
    return json.dumps(response_dict), status_code


@app.route('/user/me/photos', methods=['GET'])
@ValidateToken
def get_my_photos(*args, **kwargs):
    photos_page = photo_client.get_stubbed_photos(kwargs.get('user'), request.args.get('last_id'))
    return json.dumps(list(map(Photo.to_dict, photos_page))), HTTP_STATUS_OK


@app.route('/photo', methods=['POST'])
@ValidateToken
def post_photo(*args, **kwargs):
    response_dict, status_code = photo_client.post_photo(kwargs.get('user'), request)
    return json.dumps(response_dict), status_code


@app.route('/following/photos', methods=['GET'])
@ValidateToken
def get_photos_for_feed(*args, **kwargs):
    response_dict, status_code = photo_client.get_photos_for_feed(kwargs.get('user'), request.args.get('last_id'))
    return json.dumps(response_dict), status_code


# Since everything that we return will literally be a json, might as well use @app.after_request
# instead of attaching a custom annotation (aka decorators in Python land)
@app.after_request
def set_content_type(response):
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    app.run()
