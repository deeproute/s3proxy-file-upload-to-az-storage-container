#!/usr/local/bin/python3

import boto3
from botocore.errorfactory import ClientError
import os
import glob
import json
import time
import logging

def upload_file(s3_client, file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def main():
    aws_endpoint = os.getenv('AWS_S3_ENDPOINT')
    access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket_name = os.getenv('BUCKET_NAME')

    upload_file_name = 'test-file.txt'

    print(f'AWS_S3_ENDPOINT: {aws_endpoint}')
    print(f'AWS_ACCESS_KEY_ID: {access_key_id}')
    print(f'AWS_SECRET_ACCESS_KEY: ****')
    print(f'BUCKET_NAME: {bucket_name}')

    s3_client = boto3.client(
        service_name = 's3',
        aws_access_key_id = access_key_id,
        aws_secret_access_key = secret_access_key,
        endpoint_url = aws_endpoint
    )

    print(f'Uploading File: {upload_file_name}')

    upload_file(s3_client, upload_file_name, bucket_name)

    print(f'Upload Complete.')

main()
