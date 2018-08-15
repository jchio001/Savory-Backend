from status_codes import HTTP_STATUS_OK, HTTP_STATUS_BAD_REQUEST

import json
import logging
import os
import requests

fb_app_id = os.environ['SAVORY_FB_APP_ID']
fb_app_secret = os.environ['SAVORY_FB_APP_SECRET']

fb_graphql_url = 'https://graph.facebook.com/v3.1'

long_lived_token_url = '/oauth/access_token?grant_type=fb_exchange_token&' \
                       'client_id=%d&client_secret=%s&fb_exchange_token=%s'
id_uri = '/me?fields=id,first_name,last_name,picture&access_token=%s'

# Generic error logging template
logging_error_template = 'Error received for %s. Http status code: %d, Response body: %s'


def get_profile(token):
    response = requests.get(fb_graphql_url + id_uri % token)
    content_json = json.loads(response.content)
    if response.status_code == HTTP_STATUS_OK:
        if 'error' in content_json:
            logging.error(logging_error_template, get_profile.__name__,
                          response.status_code, response.content)
            raise FacebookException(response)
        else:
            logging.info('%s received a successful response from the server %s',
                         get_profile.__name__, response.content)
            return FacebookAccount(content_json)
    else:
        logging.error(logging_error_template, get_profile.__name__,
                      response.status_code, response.content)
        raise FacebookException(response)


def create_facebook_error_response():
    return {'message': 'Invalid facebook token.'}, HTTP_STATUS_BAD_REQUEST


class FacebookAccount:
    def __init__(self, response_dict):
        self.id = response_dict.get('id')
        self.first_name = response_dict.get('first_name')
        self.last_name = response_dict.get('last_name')
        self.profile_image = response_dict.get('picture').get('data').get('url')


class FacebookException(Exception):
    def __init__(self, response):
        self.status_code = response.status_code
        self.error_body = response.content
