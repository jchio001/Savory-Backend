from boto3.exceptions import S3UploadFailedError
from models import Photo, session
from status_codes import HTTP_STATUS_OK, HTTP_STATUS_BAD_REQUEST

import logging
import s3_client


def post_photo(account, request):
    if 'image' not in request.files:
        return {'error': 'No image attached!'}, HTTP_STATUS_BAD_REQUEST

    file = request.files['image']

    try:
        account_id = account.id

        photo_url = s3_client.upload_photo(account_id, file)

        photo = Photo(account_id=account_id, photo_url=photo_url)
        session.add(photo)
        session.flush()
        session.commit()

        return photo.to_dict(), HTTP_STATUS_OK
    except S3UploadFailedError as e:
        logging.error(str(e))
        return {'error': 'Failed to upload image!'}, HTTP_STATUS_BAD_REQUEST