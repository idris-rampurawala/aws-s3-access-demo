from datetime import datetime
from os import environ
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def create_presigned_url(
        bucket_name: str, object_name: str, expiration=3600) -> Optional[str]:
    """Generate a presigned URL to share an s3 object

    Arguments:
        bucket_name {str} -- Required. s3 bucket of object to share
        object_name {str} -- Required. s3 object to share

    Keyword Arguments:
        expiration {int} -- Expiration in seconds (default: {3600})

    Returns:
        Optional[str] -- Presigned url of s3 object. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    aws_profile = environ.get('AWS_PROFILE_NAME')
    s3_client = boto3.session.Session(
        profile_name=aws_profile).client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={
                                                        'Bucket': bucket_name,
                                                        'Key': object_name
                                                    },
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def rsa_signer(message: str) -> str:
    with open('.cloudfront-pk.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key.sign(
        message, padding.PKCS1v15(), hashes.SHA1())


def create_cloudfront_signed_url(
        object_name: str, expiration_date: datetime) -> str:
    """Generate a cloudfront signed URL to share an s3 object

    Arguments:
        object_name {str} -- Required. s3 object to share
        expiration_date {datetime} -- Required. Expiration datetime object of
                                        some future datetime

    Returns:
        str -- cloudfront signed URL
    """
    key_id = environ.get('AWS_CLOUDFRONT_USER_ACCESS_ID')
    url = '{cloudfront_domain}/{object_name}'.format(
        cloudfront_domain=environ.get('AWS_CLOUDFRONT_DOMAIN'),
        object_name=object_name
    )

    cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)

    # Create a signed url that will be valid until the specfic expiry date
    # provided using a canned policy.
    signed_url = cloudfront_signer.generate_presigned_url(
        url, date_less_than=expiration_date)
    return signed_url
