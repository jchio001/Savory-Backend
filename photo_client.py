from boto3.exceptions import S3UploadFailedError
from datetime import datetime
from models import Photo, session
from status_codes import HTTP_STATUS_OK, HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_INTERNAL_SERVER_ERROR
from sqlalchemy import desc

import account_client
import google_places_client
import logging
import s3_client


def post_photo(account, request):
    place_id = request.form.get('place_id')
    if not place_id:
        return {'error': 'Missing place_id.'}, HTTP_STATUS_BAD_REQUEST

    place_response = google_places_client.get_google_place(place_id)
    if place_response:
        if not place_response.is_successful():
            return {'error': 'Invalid place_id.'}, HTTP_STATUS_BAD_REQUEST
    else:
        return {'error': 'Google places API error. Try again later'}, HTTP_STATUS_INTERNAL_SERVER_ERROR

    if 'image' not in request.files:
        return {'error': 'No image attached!'}, HTTP_STATUS_BAD_REQUEST

    file = request.files.get('image')

    try:
        account_id = account.id
        place = place_response.place

        photo_url = s3_client.upload_photo(account_id, file)

        photo = Photo(account_id=account_id,
                      photo_url=photo_url,
                      google_place_id=place.place_id,
                      google_place_name=place.name)

        session.add(photo)
        session.flush()
        session.commit()

        return photo.to_dict(), HTTP_STATUS_OK
    except S3UploadFailedError as e:
        logging.error(str(e))
        return {'error': 'Failed to upload image!'}, HTTP_STATUS_BAD_REQUEST


STUBBED_PHOTO_URL = 'https://pbs.twimg.com/media/CgM7-d2XIAAaZ3m.jpg'


# Returns a page of 15 photos.
def get_stubbed_photos(account=None, last_id=None):
    stubbed_page = list()

    photo = Photo(id=32432, account_id=23432423, photo_url=STUBBED_PHOTO_URL, creation_date=datetime.today())
    for i in range(0, 15):
        stubbed_page.append(photo)

    return stubbed_page


def get_photos(account_ids, last_id, page_size=15):
    photo_page_query = session.query(Photo)

    if last_id:
        photo_page_query = photo_page_query.filter(Photo.id < last_id)

    return photo_page_query.filter(Photo.account_id.in_(account_ids))\
        .order_by(desc(Photo.creation_date)) \
        .limit(page_size)


def get_photos_for_feed(account, last_id):
    following_account_ids = account_client.get_following_accounts(account)
    photos_page = get_photos(following_account_ids, last_id, 10)
    return list(map(Photo.to_dict, photos_page)), HTTP_STATUS_OK
