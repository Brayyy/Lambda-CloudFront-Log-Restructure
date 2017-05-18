# Lambda CloudFront Log Restructure
---
A simple Lambda script to restructure CloudFront logs in S3 to a directory structure more useful for AWS Athena or EMR.

CloudFront does not allow log paths to be customized, aside from Bucket and prefix. This causes a problem for services such as AWS Athena and Elastic Map Reduce, which benefit from partitioned data paths. This script can copy or move the files created by CloudWatch instantly and automatically.

This script will adjust CloudFront logs structure as so:
```
s3://YOUR-BUCKET/raw/E1234567890/E1234567890.2017-02-24-23.0123abcd.gz
To this:
s3://YOUR-BUCKET/structured/E1234567890/2017/02/14/23/E1234567890.2017-02-24-23.0123abcd.gz
```

- Function is triggered by S3 as soon as CloudFront writes a log file.
- Function can be set to move or only copy the log files.
- If S3 triggers Lambda with multiple records, function will handle each correctly.
- Function can handle multiple CloudFront distributions.

Install / setup:
1. Create a new blank Python 2.7 Lambda function
2. Set up an S3 trigger
-- Bucket: Where you write your CloudFront logs
-- Event type: Object Created (All)
-- Prefix: raw/
-- Enable trigger: [true]
3. At the bottom of the "Configure function" page, set Role to "Create a custom role", it will open a new tab
-- Role Description: Lambda execution role permissions
-- IAM Role: Create new IAM Role
-- Role Name: Lambda_CloudFront-log-restructure (or whatever you want)
-- Select Allow
4. Back on "Configure function" page:
-- Name: CloudFront-log-restructure
-- Description: Restructures CloudFront logs in S3 to a directory structure more useful for AWS Athena or EMR
-- Runtime: Python 2.7
-- Code entry type: Edit code inline
-- [paste entire contents of index.py to code area]
-- Handler: index.lambda_handler
-- Role: Choose an existing role
-- Existing role: Lambda_CloudFront-log-restructure
-- Memory (MB): 128
-- Timeout: 5 seconds
5. Go into IAM and edit the newly created Role "Lambda_CloudFront-log-restructure"
-- On the permissions tab, add an inline policy named "S3-Access", with the following content:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::YOUR-BUCKET-awslogs-cloudfront/raw/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::YOUR-BUCKET-awslogs-cloudfront/structured/*"
            ]
        }
    ]
}
```
6. Edit your CloudFront distrobution(s) to write their logs to the S3 bucket with the previx "raw/"
