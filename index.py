# This Lambda function is triggered by CloudFront log files arriving in S3.
# The purpose is to move log files from the structure that CloudFront uses
# to a folder structure which is allows for partitioning within AWS Athena.
#
# https://github.com/Brayyy/Lambda-EBS-Snapshot-Manager
# Initial release 2017.05.17 - Bray Almini

import boto3


def lambda_handler(event, context):
    s3 = boto3.client('s3')

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        distro = key.split('/')[1]
        filename = key.split('/')[2]
        meta = key.split('.')[1].split('/')[0]
        year, month, day, hour = meta.split('-')
        dest = 'structured/{}/{}/{}/{}/{}/{}'.format(
            distro, year, month, day, hour, filename
        )

        print "- src: s3://%s/%s" % (bucket, key)
        print "- dst: s3://%s/%s" % (bucket, dest)

        s3.copy_object(Bucket=bucket, Key=dest, CopySource=bucket + '/' + key)
        # Disable this line if a copy is sufficient
        s3.delete_object(Bucket=bucket, Key=key)
