import boto3
import os
import time

#list all objects from a bucket and write the to a file
def ls_objects_file (bucket_name, file_name):
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(bucket_name)

	print('---LISTING OBJECTS FROM:',bucket.name,'->',file_name + '\n')

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
	print('---START COPYING OBJECTS:',bucket_old,'=>',bucket_new + '\n')
	with open(objects_list, 'r') as file_objects:
		for s3_object in file_objects:
			s3_object = s3_object.replace('\n', '')

			copy_source = {
				'Bucket': bucket_old,
				'Key': s3_object
			}

			if not object_moved(s3_object, newbucket['Moved_Log']):
				print('INFO: Copying object:', copy_source['Bucket'], copy_source['Key'], '=>', bucket_new)
				start_time_copy = time.time()

				try:
					s3 = boto3.resource('s3')
					bucket = s3.Bucket(bucket_new)
					bucket.copy(copy_source, s3_object)
				except:
					print('ERROR: Object copy error =>', copy_source['Key'])
				else:
					with open(newbucket['Moved_Log'],'a') as file_moved:
						file_moved.write(copy_source['Key'] + '\n')
					print('INFO: Object moved =>', copy_source['Key'])

				print('Execution time: ' + str((time.time() - start_time_copy)) + '\n')
			else:
				print('WARN: OBJECT ALREADY MOVED ->', s3_object)

#count objects from a bucket
def count_objects(bucket):
	totalCount = 0
	for key in bucket.objects.all():
		totalCount += 1
	return totalCount

#compare the number of objects from two buckets
def compare_buckets(bucket1, bucket2):
	s3 = boto3.resource('s3')
	print('INFO:',bucket1,'->',count_objects(s3.Bucket(bucket1)),'objects found.')
	print('INFO:',bucket2,'->',count_objects(s3.Bucket(bucket2)),'objects found.')
	return count_objects(s3.Bucket(bucket1)) == count_objects(s3.Bucket(bucket2))

#remove a file
def remove_file(file):
		if os.path.isfile(file):
			os.remove(file)
			print('INFO: File',file,'removed.')
		else:
			print('ERROR: The file',file,'does not exist.')

#empty a bucket
def empty_bucket(bucket_name):
	try:
		s3 = boto3.resource('s3')
		bucket = s3.Bucket(bucket_name)
		bucket.objects.all().delete()
	except Exception as e:
		print('ERROR: Clean bucket error ->',e)
	else:
		print('INFO: Bucket',bucket_name,'empty.')

#delete a bucket
def delete_bucket(bucket_name):
	try:
		s3 = boto3.resource('s3')
		bucket = s3.Bucket(bucket_name)
		bucket.delete()
	except Exception as e:
		print('ERROR: Delete bucket error ->',e)
	else:
		print('INFO: Bucket',bucket_name,'deleted.')

#cleaning operations
def clean_ops(oldbucket, newbucket):
	print('---CLEANING OPERATIONS')
	if compare_buckets(oldbucket['Name'], newbucket['Name']):
		try:
			remove_file(oldbucket['File'])
			remove_file(newbucket['File'])
			remove_file(newbucket['Moved_Log'])
			empty_bucket(oldbucket['Name']),
			#delete_bucket(oldbucket['Name']),
			compare_buckets(oldbucket['Name'], newbucket['Name'])
		except:
			print('ERROR: Clean operations failed.')
		finally:
			print('INFO: PROGRAM FINISHED.'+ '\n')
	else:
		print('ERROR: Different number of objects detected on both buckets. Please check.')

#main function
def main():
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

	ls_objects_file(oldbucket['Name'],oldbucket['File'])
	cp_objects(oldbucket['Name'], oldbucket['File'], newbucket['Name'])
	ls_objects_file(newbucket['Name'],newbucket['File'])
	clean_ops(oldbucket,newbucket)

	print('\n' + '---TOTAL EXECUTION TIME: ' + str((time.time() - start_time)) + '\n')

if __name__ == "__main__":
    main()


