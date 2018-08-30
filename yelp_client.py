from status_codes import HTTP_STATUS_OK

import json
import os
import requests

restaurant_details_base_url = 'https://api.yelp.com/v3/businesses/{}'

yelp_api_key = os.environ['SAVORY_YELP_API_KEY']

headers = {'Authorization': 'Bearer {}'.format(yelp_api_key)}


def get_restaurant(yelp_restaurant_id):
    yelp_restaurant_details_response = requests.get(restaurant_details_base_url.format(yelp_restaurant_id),
                                                    headers=headers)
    if yelp_restaurant_details_response.status_code == HTTP_STATUS_OK:
        return YelpRestaurant(json.loads(yelp_restaurant_details_response.content))


class YelpRestaurant:
    def __init__(self, yelp_restaurant_details_dict):
        self.id = yelp_restaurant_details_dict.get('id')
        self.name = yelp_restaurant_details_dict.get('name')
