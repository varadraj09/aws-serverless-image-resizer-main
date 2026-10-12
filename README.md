# AWS Serverless Image Resizer

## Project Overview

This project automatically resizes images uploaded to an Amazon S3 source bucket using AWS Lambda and Python. The resized images are saved in a separate Amazon S3 destination bucket.

## Architecture

1. An image is uploaded to the source S3 bucket.
2. An S3 event triggers the AWS Lambda function.
3. Lambda uses Python and Pillow to resize the image.
4. The resized image is saved to the destination S3 bucket.

## AWS Services Used

* **Amazon S3** — stores original and resized images
* **AWS Lambda** — runs the image-resizing function
* **Amazon CloudWatch** — monitors execution logs
* **Python** — implements the processing logic
* **Pillow** — image-processing library

## Project Structure

```text
aws-serverless-image-resizer/
├── lambda_function.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

* An AWS account
* An S3 source bucket and destination bucket
* An AWS Lambda function with a compatible Python runtime
* Pillow compatible with the Lambda runtime and architecture

## Configuration

Configure the Lambda environment variable:

* `DESTINATION_BUCKET` — name of the S3 bucket where resized images are stored.

Configure an S3 event notification on the source bucket to invoke the Lambda function. Ensure the Lambda execution role has the necessary permissions to read source objects and write destination objects.

## Deployment Notes

Package Pillow and its native dependencies for the same Python runtime and architecture used by Lambda. Upload the deployment package to Lambda and configure the handler as:

`lambda_function.lambda_handler`

## Testing

1. Upload a supported image to the source S3 bucket.
2. Check the Lambda invocation in Amazon CloudWatch.
3. Verify that the resized image appears in the destination bucket.

## Security

Do not commit AWS access keys, secret keys, private configuration files, or sensitive bucket information to GitHub.

## Learning Outcomes

* Event-driven serverless architecture
* S3 event notifications
* AWS Lambda deployment and configuration
* Python image processing
* CloudWatch troubleshooting and monitoring

