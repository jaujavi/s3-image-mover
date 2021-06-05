import boto3
import os
import time

def cp_object (bucket_old, file_name, bucket_new):

	file = open(file_name, 'r')
	for s3_object in file:

		s3_object = s3_object.replace('\n', '')

		start_time_copy = time.time()

		copy_source = {
			'Bucket': bucket_old,
			'Key': s3_object
		}

		print('COPYING:', copy_source['Bucket'], copy_source['Key'], '=>', bucket_new)
		s3 = boto3.resource('s3')
		bucket = s3.Bucket(bucket_new)
		bucket.copy(copy_source, s3_object)

		print('Execution time: ' + str((time.time() - start_time_copy)) + '\n')

	file.close()

#main

oldbucket = {
	'name':'jaujavi-oldbucket',
	'file':'s3_oldbucket_objects.txt'
}

newbucket = {
	'name':'jaujavi-newbucket',
	'file':'s3_newbucket_objects.txt'
}

start_time = time.time()
print('---START COPYING' + '\n')

cp_object(oldbucket['name'], oldbucket['file'], newbucket['name'])

print('---TOTAL EXECUTION TIME: ' + str((time.time() - start_time)) + '\n')