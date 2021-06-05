import boto3
import os

s3_oldbucket = 'jaujavi-oldbucket'
s3_newbucket = 'jaujavi-newbucket'

s3_oldbucket_file = open('s3_oldbucket_objects.txt','w')
s3_newbucket_file = open('s3_newbucket_objects.txt','w')

s3 = boto3.resource('s3')
oldbucket = s3.Bucket(s3_oldbucket)
print('=> LISTING OBJECTS FROM:',s3_oldbucket)
for s3_file in oldbucket.objects.all():
    #print(s3_file.key)
	s3_oldbucket_file.write(s3_file.key + '\n')