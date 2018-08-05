from boto3.exceptions import S3UploadFailedError
from models import Photo, session

import logging
import s3_client
import savory_token_client


def post_photo(request):
    if 'image' not in request.files:
        return {'error': 'No image attached!'}

    file = request.files['image']

    try:
        account_id = savory_token_client \
            .decode_savory_token(request.headers.get('Authorization')) \
            .get('id')

        photo_url = s3_client.upload_photo(account_id, file)

        photo = Photo(account_id=account_id, photo_url=photo_url)
        session.add(photo)
        session.flush()
        session.commit()

        return photo.to_dict()
    except S3UploadFailedError as e:
        logging.error(str(e))
        return {'error': 'Failed to upload image!'}