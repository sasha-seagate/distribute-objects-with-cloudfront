import boto3
import os
from botocore.client import Config

# Set the access key ID and secret access key
access_key_id = os.environ['ACCESS_KEY']
secret_access_key = os.environ['SECRET_KEY']

# Set the bucket name, object key, endpoint and expiration time (in seconds)
bucket_name = os.environ['BUCKET_NAME']
object_key = os.environ['OBJECT_KEY']
expiration = os.environ['EXPIRATION']
endpoint = os.environ['ENDPOINT']

# Create an S3 client
client = boto3.client(
    "s3",
    endpoint_url=endpoint,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    config=Config(signature_version="s3v4"),
)

def lambda_handler(event, context):
    # Generate the presigned URL
    presigned_url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expiration,
    )
    
    # Return the signed URL to CloudFront as the response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
            
        },
        'body': '<a href><img src='+presigned_url+'></a>'
        
    }