from werkzeug.utils import secure_filename
from boto3.exceptions import S3UploadFailedError
from models import Photo, session

import boto3
import logging
import os
import savory_token_client

s3_url_template = 'https://s3-%s.amazonaws.com/%s/%s'
aws_access_key_id = os.environ['SAVORY_AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['SAVORY_AWS_SECRET_KEY']
bucket_name = 'savory-debug'
bucket_location = 'us-west-1'


s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


def post_photo(request):
    if 'image' not in request.files:
        return {'error': 'No image attached!'}

    file = request.files['image']
    file_name = secure_filename(file.filename)
    logging.info(file_name)

    try:
        s3_client.upload_fileobj(file, bucket_name, file_name, {'ACL': 'public-read'})

        account_id = savory_token_client \
            .decode_savory_token(request.headers.get('Authorization')) \
            .get('id')

        photo = Photo(account_id=account_id,
                      photo_url=s3_url_template % (bucket_location, bucket_name, file_name))
        session.add(photo)
        session.flush()
        session.commit()

        return photo.to_dict()
    except S3UploadFailedError as e:
        logging.error(str(e))
        return {'error': 'Failed to upload image!'}