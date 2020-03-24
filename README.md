# AWS S3 Object Access Demo

> Share Your AWS S3 Private Object With Others Without Making It Public

This project is an implementation to show various approaches to share your AWS S3 private object with others without making it public. You can find an in-depth article on this implementation [here](https://dev.to/idrisrampurawala/share-your-aws-s3-private-content-with-others-without-making-it-public-4k59).

## Background

Amazon Web Services (AWS) S3 objects are private by default. Only the object owner has permission to access these objects. Optionally we can set `bucket policy` to whitelist some accounts or URLs to access the objects of our S3 bucket.

There are various instances where we want to share our S3 object with users temporarily or with some specific expiration time without the need to make our S3 bucket private. This project aims to solve that problem by creating `presigned url` with some code examples.

## Prerequisites

- Python 3.7.2 or higher
- Install `pip`
- AWS account with an S3 bucket and an object
- `aws-cli` configured locally

## Virtual Env

- Install `virtualenv` a global python project

## Configuration

- Create a file `.env` in the root from `.env.example`
- Add appropriate values for the project to run in `.env`
- If you are using `CloudFront` approach of creating signed url, then please add a private key with the name `.cloudfront-pk.pem` (at the root of the project) of IAM user to allow it to generate the url

## Running app

- Create a `virtual environment` for this project `virtualenv aws-s3-access-env`
- Activate virtual environment
- Install dependencies `pip install -r requirements.txt`
- Run flask app `flask run`

## License

MIT
