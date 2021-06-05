import boto3
import os

def list_objects_file (bucket_name, file_name):
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(bucket_name)

	print('=> LISTING OBJECTS FROM:',bucket)

	objects_file = open(file_name,'w')
	for s3_object in bucket.objects.all():
    	#print(s3_object.key)
		objects_file.write(s3_object.key + '\n')

#main
s3_oldbucket = 'jaujavi-oldbucket'
s3_newbucket = 'jaujavi-newbucket'

s3_oldbucket_file = 's3_oldbucket_objects.txt'
s3_newbucket_file = 's3_newbucket_objects.txt'

list_objects_file(s3_oldbucket,s3_oldbucket_file)
list_objects_file(s3_newbucket,s3_newbucket_file)