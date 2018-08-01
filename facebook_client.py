import json
import logging
import os
import requests

from status_codes import HTTP_STATUS_OK, HTTP_STATUS_BAD_REQUEST

# TODO: DON'T EXPOSE THIS
fb_app_id = os.environ['SAVORY_FB_APP_ID']
fb_app_secret = os.environ['SAVORY_FB_APP_SECRET']

fb_graphql_url = 'https://graph.facebook.com/v3.1'

long_lived_token_url = '/oauth/access_token?grant_type=fb_exchange_token&' \
                       'client_id=%d&client_secret=%s&fb_exchange_token=%s'
id_uri = '/me?fields=id,first_name,last_name,picture&access_token=%s'

# Generic error logging template
logging_error_template = 'Error received for %s. Http status code: %d, Response body: %s'


# Given a response object, transform it into a FacebookResponse object
def response_to_facebook_response(response, method_name):
    content_json = json.loads(response.content)
    if response.status_code == HTTP_STATUS_OK:
        if 'error' in content_json:
            logging.error(logging_error_template, method_name,
                          response.status_code, response.content)
        else:
            logging.info('%s received a successful response from the server %s',
                         method_name, response.content)
    else:
        logging.error(logging_error_template, method_name,
                      response.status_code, response.content)

    return FacebookResponse(response.status_code, content_json)


def get_profile(token):
    response = requests.get(fb_graphql_url + id_uri % token)
    return response_to_facebook_response(response, get_profile.__name__)


def create_facebook_error_response():
    return {'message': 'Invalid facebook token.'}, HTTP_STATUS_BAD_REQUEST


# Class that wraps around a response from Facebook's Graph API
class FacebookResponse:
    def __init__(self, status_code, response_dict):
        self.status_code = status_code
        self.response_dict = response_dict

    def is_successful(self):
        return self.status_code == HTTP_STATUS_OK and 'error' not in self.response_dict