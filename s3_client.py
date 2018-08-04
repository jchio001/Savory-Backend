from werkzeug.utils import secure_filename

import boto3
import logging
import os

s3_url_template = 'https://s3-%s.amazonaws.com/%s/%s'
aws_access_key_id = os.environ['SAVORY_AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['SAVORY_AWS_SECRET_KEY']
bucket_name = 'savory-debug'
bucket_location = 'us-west-1'

s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


# Uploads a photo to the S3 bucket and returns an image url that points to it.
# If this fails, it will throw a boto3.exceptions.S3UploadFailedError.
def upload_photo(file):
    file_name = secure_filename(file.filename)
    logging.info('Uploading file %s to S3 Bucket' % file_name)
    s3_client.upload_fileobj(file, bucket_name, file_name, {'ACL': 'public-read'})
    return s3_url_template % (bucket_location, bucket_name, file_name)