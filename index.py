# This Lambda function is triggered by CloudFront log files arriving in S3.
# The purpose is to move log files from the structure that CloudFront uses
# to a folder structure which is allows for partitioning within AWS Athena.
#
# https://github.com/Brayyy/Lambda-CloudFront-Log-Restructure
# Initial release 2017.05.17 - Bray Almini

import boto3


def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Iterate over all records in the list provided
    for record in event['Records']:

        # Get the S3 bucket
        bucket = record['s3']['bucket']['name']
        # Get the source S3 object key
        key = record['s3']['object']['key']
        # Get the CloudFront distribution id from the source S3 object
        distro = key.split('/')[1]
        # Get just the filename of the source S3 object
        filename = key.split('/')[2]
        # Get the yyyy-mm-dd-hh from the source S3 object
        dateAndHour = key.split('.')[1].split('/')[0]
        year, month, day, hour = dateAndHour.split('-')
        # Create destination path
        dest = 'structured/{}/{}/{}/{}/{}/{}'.format(
            distro, year, month, day, hour, filename
        )

        # Display source/destination in Lambda output log
        print "- src: s3://%s/%s" % (bucket, key)
        print "- dst: s3://%s/%s" % (bucket, dest)

        # Perform copy of the S3 object
        s3.copy_object(Bucket=bucket, Key=dest, CopySource=bucket + '/' + key)

        # Delete the source S3 object
        # Disable this line if a copy is sufficient
        s3.delete_object(Bucket=bucket, Key=key)
