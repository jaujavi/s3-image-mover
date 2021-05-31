import boto3

myloc = 'eu-west-3'
mybucket = 'jaujavi-bucket02'
#s3 = boto3.client('s3')
s3 = boto3.resource('s3')

# Print out bucket names
print("S3 bucket list:")
for bucket in s3.buckets.all():
    print(bucket.name)

# Create bucket
print("Creating bucket S3...")
location = {'LocationConstraint': myloc}
s3.create_bucket(Bucket=mybucket,CreateBucketConfiguration=location)

# Print out bucket names
print("S3 bucket list:")
for bucket in s3.buckets.all():
    print(bucket.name)

# Retrieve the list of existing buckets
#response = s3.list_buckets()

# Output the bucket names
#print('Existing buckets:')
#for bucket in response['Buckets']:
#    print(f'  {bucket["Name"]}')