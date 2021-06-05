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


#determine if an object is already copied or not
def object_moved (object_name, file_name):
	try:
		with open(file_name, 'r') as file_moved:
			if object_name in file_moved.read():
				return True
			else:
				return False
	except IOError:
		print('WARN: File', file_name,'not exists. Maibe it is the first execution.\n')
		return False


#copy all objects from a list from one bucket to another
def cp_objects (bucket_old, objects_list, bucket_new):

	with open(objects_list, 'r') as file_objects:
		for s3_object in file_objects:
			s3_object = s3_object.replace('\n', '')

			copy_source = {
				'Bucket': bucket_old,
				'Key': s3_object
			}

			if not object_moved(s3_object, newbucket['Moved_Log']):
				print('COPYING:', copy_source['Bucket'], copy_source['Key'], '=>', bucket_new)
				start_time_copy = time.time()

				try:
					#s3 = boto3.resource('s3')
					#bucket = s3.Bucket(bucket_new)
					#bucket.copy(copy_source, s3_object)
					print('--- bucket opetation ---')
				except:
					print('COPY ERROR =>', copy_source['Key'])
				else:
					with open(newbucket['Moved_Log'],'a') as file_moved:
						file_moved.write(copy_source['Key'] + '\n')
					print('OBJECT MOVED =>', copy_source['Key'])

				print('Execution time: ' + str((time.time() - start_time_copy)) + '\n')
			else:
				print('WARN: OBJECT ALREADY MOVED ->', s3_object)


#---main

oldbucket = {
	'Name':'jaujavi-oldbucket',
	'File':'s3_oldbucket_objects.txt'
}

newbucket = {
	'Name':'jaujavi-newbucket',
	'File':'s3_newbucket_objects.txt',
	'Moved_Log':'s3_moved_objects.log'
}

start_time = time.time()
print('---START COPYING' + '\n')

ls_objects_file(oldbucket['Name'],oldbucket['File'])
cp_objects(oldbucket['Name'], oldbucket['File'], newbucket['Name'])
ls_objects_file(newbucket['Name'],newbucket['File'])

print('---TOTAL EXECUTION TIME: ' + str((time.time() - start_time)) + '\n')