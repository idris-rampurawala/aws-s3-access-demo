from datetime import datetime, timedelta
from os import environ

from dotenv import load_dotenv
from flask import Flask
from utils import create_cloudfront_signed_url, create_presigned_url

# loading env vars from .env file
load_dotenv()
app = Flask(__name__)


@app.route('/generate_presigned_url', methods=['GET'])
def generate_presigned_url():
    # creating signed url via S3
    url = create_presigned_url(
        environ.get('AWS_S3_BUCKET'),
        environ.get('AWS_S3_RESOURCE_URL')
    )
    return {
        'url': url
    }


@app.route('/generate_cloudwatch_signed_url', methods=['GET'])
def generate_cloudwatch_signed_url():
    # creating signed url via CloudFront
    expire_date = datetime.utcnow() + timedelta(days=2)
    url = create_cloudfront_signed_url(
        environ.get('AWS_S3_RESOURCE_URL'),
        expire_date
    )
    return {
        'url': url
    }


if __name__ == '__main__':
    app.run()
