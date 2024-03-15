from random import randint
import boto3
import uuid
from PIL import Image
import os

s3_client = boto3.client('s3')
     
def resize_image(image_path, resized_path):

    image = Image.open(image_path)

    required_dimensions = 1000
    if image.size[0] >= image.size[1]:
        wpercent = (required_dimensions/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((required_dimensions, hsize))
    else:
        hpercent = (required_dimensions/float(image.size[1]))
        wsize = int((float(image.size[0])*float(hpercent)))
        image = image.resize((wsize, required_dimensions))

    image.save(resized_path)
    



     
def handler(event, context):
    for record in event['Records']:

        bucket_name = record['s3']['bucket']['name']
        key_name = record['s3']['object']['key']

        download_path = '/tmp/{}'.format(os.path.basename(key_name))
        upload_path = '/tmp/resized-{}'.format(os.path.basename(key_name))

        s3_client.download_file(bucket_name, key_name, download_path)

        resize_image(download_path, upload_path)

        s3_client.upload_file(upload_path, bucket_name, 'resized-{}'.format(key_name))
#add pillow as a layer in aws lambda console