import logging
import boto3
from botocore.exceptions import ClientError

file_name = 'images/0_puppies.jpg'
bucket = 'jaujavi-oldbucket'
object_name = file_name

# Upload the file
s3_client = boto3.client('s3')
try:
	response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL':'public-read'})
	print(response)
except ClientError as e:
	logging.error(e)