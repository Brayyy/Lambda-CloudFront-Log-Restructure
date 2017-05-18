# Lambda CloudFront Log Restructure
---

CloudFront does not allow log paths to be customized, aside from Bucket and prefix. This causes a problem for services such as AWS Athena and Elastic Map Reduce, which benefit from partitioned data paths. This script can copy or move the files created by CloudWatch instantly and automatically.

- Function is triggered by S3 as soon as CloudFront writes a log file.
- Function can be set to move or only copy the log files.
- If S3 triggers Lambda with multiple records, function will handle each correctly.
- Function can handle multiple CloudFront distributions.