import logging
import boto3
from botocore.exceptions import ClientError
import os

dir_images = 'images/'
bucket_name = 'jaujavi-oldbucket'

for root, dirs, files in os.walk(dir_images):
	for file in files:
		if file.endswith(".jpg"):
			file_and_path = os.path.join(root, file)
			print(file_and_path)
			object_name = file_and_path

			# Upload the file
			s3_client = boto3.client('s3')
			try:
				response = s3_client.upload_file(file_and_path, bucket_name, object_name, ExtraArgs={'ACL':'public-read'})
				print(response)
			except ClientError as e:
				logging.error(e)