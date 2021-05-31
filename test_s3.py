import boto3

myloc = 'eu-west-3'
mybucket = 'jaujavi-bucket01'
s3 = boto3.client('s3')

# Create bucket
print("Creating bucket S3...")
location = {'LocationConstraint': myloc}
s3.create_bucket(Bucket=mybucket,CreateBucketConfiguration=location)

# Retrieve the list of existing buckets
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')