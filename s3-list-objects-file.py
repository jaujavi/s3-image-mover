import boto3
import os

def list_objects_file (bucket_name, file_name):
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(bucket_name)

	print('=> LISTING OBJECTS FROM:',bucket.name)

	objects_file = open(file_name,'w')
	for s3_object in bucket.objects.all():
    	#print(s3_object.key)
		objects_file.write(s3_object.key + '\n')

oldbucket = {
	'name':'jaujavi-oldbucket',
	'file':'s3_oldbucket_objects.txt'
}

newbucket = {
	'name':'jaujavi-newbucket',
	'file':'s3_newbucket_objects.txt'
}

list_objects_file(oldbucket['name'],oldbucket['file'])
list_objects_file(newbucket['name'],newbucket['file'])