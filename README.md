# s3-image-mover

## I need to move move a lot of files

Let's say we have 1.000 jpg images in a S3 bucket.

For example: http://s3.amazonaws.com/old_bucket/image123.jpg, http://s3.amazonaws.com/old_bucket/image124.jpg etc

I need to move all this images to a new bucket called new-bucket.

For example: http://s3.amazonaws.com/new_bucket/image123.jpg, http://s3.amazonaws.com/new_bucket/image124.jpg etc

`old_bucket` and `new_bucket` are just examples, I may use any name. There is nothing more than jpg images in the bucket.

### My task

- I need to move these 1.000 images from old-bucket to new-bucket.
- As fast as possible (in this case, speed is important)
- If the process fails for any reason, it should resume (and not start from the beginning)

### Expected

- The program to be written in any programming language. 
- The program is runnable in a UNIX-like environment, if it is easy for they to test, it would be great 😀
- To hear my thoughts on scalability and speed if the bucket contains 10.000, 100.000, 1.000.000 of images etc. (they may talk about this in the interview)
- The code of this challenge will be written in a Git repository and zipped. Try to not write the entire program in one commit and version it as much as you can. For they, understanding your progress is valuable.
- Also, if I think this can be accomplished using any other method (not a program), we would like to hear your idea.

### Some comments

- Feel free to use files, databases or whatever you like as long as I keep it simple.
- To keep this free of charge, you may use a local S3 emulation tool or AWS free tier.


## What I do

I have to say that before this challenge I had not programmed in python and this challenge has given me more knowledge of Python that I didn't kwow and It was funny working with it and learn about this language.

First of all What I did was create and configure a github account and reactivate my AWS account. I prefer using the real AWS bucket than an emulation tool. Also I created a tagged user with all permission to work with buckets (AmazonS3FullAccess) and with boundary (to control the maximum permissions this user can have).

### My thoughts

When I start thinking this challenge my preferences was using ShellScripting (Bash) to programm it casuse I'm more familiarizate with it, but I read that Python and also boto3 module was easier and more powerful than Bash for work against AWS. So, let's do it.

So before code I start [reading](https://aws.amazon.com/premiumsupport/knowledge-center/s3-large-transfer-between-buckets/) how to do it and the best practice to make it as fast as possible. Some of them:

1.- AWS CLI: I [read](https://awscli.amazonaws.com/v2/documentation/api/latest/topic/s3-config.html) the posibility to use AWS CLI for split up my transfer using --exclude and --include parameters to separate the operations by file name and [some](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html) best practices to optimize S3 performance. The problem of that option are mainly three:
- Although it is very efficient, it is not possible to have control of what was copied in case of a process crash and to pick up where it was going.
- I can't determine the objects name.
- AWS says: "If you need to transfer a very large number of objects (hundreds of millions), consider building a custom application using an AWS SDK to perform the copy. While the AWS CLI can perform the copy, a custom application might be more efficient at that scale."

2.- AWS SDK: What I choose, using the Python BOTO3 module ([S3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)). And gives you the possibility to work with multithreading execution, since it is designed to develop an efficient and scalable program.

3.- Use cross-Region replication or same-Region replication: I don't need to replicate objects. Option out of programming. And also it won’t replicate the existing objects. Cost and performance would have to be tested.

4.- Use Amazon S3 batch operations: Best option out of programming. Designed for more than 10 million objects. Cost and performance would have to be tested. 

5.- Use S3DistCp with Amazon EMR: Sure expensive. What about of reengineering?

6.- Use AWS DataSync: I don't want to sync. Option out of programming. Cost and performance would have to be tested.

### My environment
- OS: Manjaro
- Shell: zsh
- AWS region: eu-west-3
- AWS SDK: boto3
- GIT: github
- Text editor: Sublime text with Markmon
- 1000 Images: I have downloaded them with a Google Chrome [extension](https://chrome.google.com/webstore/detail/image-downloader-imageye/agionbommeaifngbhincahgmoflcikhm).

### Premises
Note that in your "oldbucket" you need some objects to work with and the new one has to be empty.
There is nothing more than JPG images in the bucket.
Both buckets are from the same account and Standar types.
There's no ACLs on objects neither versioning.
Data isn't encrypted.
Thers's no objects more than 5GB of size.

### Implementig
I think that the most important things about this challenge is that if the process fails for any reason it should resume, and it should run as fast as possible. So,let's do it.

To make it possible I develop three principal functions:
- Listing objects from a bucket.
- Copying object between buckets.
- Empty [and delete] source bucket and other ops.
- Other basic funtions like compare and count objects, empty and delete bucket and remove files.

Also I print warning, info and error texts during the execution.

The secuence is:
- List object from source bucket to a file.
- Copy those objects to a destination bucket writing each one to a file and registering the execution time.
- When finished, then it list the objects from the destination bucket and compare with the original list from the source bucket.
- If the programm failed, it will resume from the copying list file.
- Finally it compares the number of objects from the source bucket with those from the destination bucket. clean al files that it generate, and empty all the objects from the source bucket. Optionally it could delete source bucket.
- When finished, it will write the total execution time.

### How to run it

- Configure the user you want to work with buckets:
```bash
$ aws configure
```
- Replace the buckets name with yours:
```python
	'Name':'jaujavi-oldbucket',
	'Name':'jaujavi-newbucket',
```
- Execute
```bash
$ python s3-image-mover.py
```
### Testing

- Copying 1000 objects (JPG files) took arround 6 minutes, between 0,3s and 0,4s each one.
- When I killed the program and I start it again, it resumes where it left off.

### Future improvements
- Python Multitheading.
- Sharding the object list
- Multiple programm execution.
- Compare all objects one by one, not only the number of objects from the buckets.
- PEP8 and pycodestyle python programming best practices.

### Other best practices applied
- MFA for AWS sing in.
- Tagging all objects on AWS.
- Least privilege principle.