import json
import os
import requests

from status_codes import HTTP_STATUS_OK

GOOGLE_PLACES_API_KEY = os.environ['SAVORY_GOOGLE_PLACES_API_KEY']
PLACE_DETAILS_BASE_URL = 'https://maps.googleapis.com/maps/api/place/details/json?key=' + GOOGLE_PLACES_API_KEY \
                         + '&place_id={}&fields=place_id,name'


def get_google_place(place_id):
    if place_id:
        google_place_response = requests.get(PLACE_DETAILS_BASE_URL.format(place_id))

        if google_place_response.status_code == HTTP_STATUS_OK:
            print(google_place_response.content)
            return PlaceResponse(json.loads(google_place_response.content))


class Place:
    def __init__(self, google_place_result_dict):
        self.place_id = google_place_result_dict.get('place_id')
        self.name = google_place_result_dict.get('name')


class PlaceResponse:
    def __init__(self, google_place_dict):
        self.status = google_place_dict.get('status')

        if self.status and 'result' in google_place_dict:
            self.place = Place(google_place_dict.get('result'))

    def is_successful(self):
        return self.status == 'OK' and self.place is not None
