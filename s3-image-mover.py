import boto3
import os
import time

#list all objects from a bucket and write the to a file
def ls_objects_file (bucket_name, file_name):
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(bucket_name)

	print('=> LISTING OBJECTS FROM:',bucket.name)

	objects_file = open(file_name,'w')
	for s3_object in bucket.objects.all():
    	#print(s3_object.key)
		objects_file.write(s3_object.key + '\n')


#copy all objects from a list from one bucket to another
def cp_objects (bucket_old, file_name, bucket_new):

	file_objects = open(file_name, 'r')
	file_moved = open(newbucket['Moved'],'w')

	for s3_object in file_objects:

		s3_object = s3_object.replace('\n', '')

		start_time_copy = time.time()

		copy_source = {
			'Bucket': bucket_old,
			'Key': s3_object
		}

		print('COPYING:', copy_source['Bucket'], copy_source['Key'], '=>', bucket_new)

		try:
			#s3 = boto3.resource('s3')
			#bucket = s3.Bucket(bucket_new)
			#bucket.copy(copy_source, s3_object)
			print('--- bucket opetation ---')
		except:
			print('COPY ERROR =>', copy_source['Key'])
		else:
			file_moved.write(copy_source['Key'] + '\n')
			print('OBJECT MOVED =>', copy_source['Key'])

		print('Execution time: ' + str((time.time() - start_time_copy)) + '\n')

	file_objects.close()
	file_moved.close()


#---main

oldbucket = {
	'Name':'jaujavi-oldbucket',
	'File':'s3_oldbucket_objects.txt'
}

newbucket = {
	'Name':'jaujavi-newbucket',
	'File':'s3_newbucket_objects.txt',
	'Moved':'s3_moved_objects.log'
}

start_time = time.time()
print('---START COPYING' + '\n')

ls_objects_file(oldbucket['Name'],oldbucket['File'])
cp_objects(oldbucket['Name'], oldbucket['File'], newbucket['Name'])
ls_objects_file(newbucket['Name'],newbucket['File'])

print('---TOTAL EXECUTION TIME: ' + str((time.time() - start_time)) + '\n')