from os import environ

from dotenv import load_dotenv
from flask import Flask

from utils import create_presigned_url

# loading env vars from .env file
load_dotenv()
app = Flask(__name__)


@app.route('/generate_presigned_url', methods=['POST'])
def generate_presigned_url():
    url = create_presigned_url(
        environ.get('AWS_S3_BUCKET'),
        environ.get('AWS_S3_RESOURCE_URL')
    )
    return {
        'url': url
    }


if __name__ == '__main__':
    app.run()
