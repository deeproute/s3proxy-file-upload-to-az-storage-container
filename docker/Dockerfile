FROM python:3.7-alpine

WORKDIR /scripts

RUN pip install boto3

COPY s3_upload.py /scripts/s3_upload.py
COPY test-file.txt /scripts/test-file.txt

RUN chmod a+x /scripts/s3_upload.py
