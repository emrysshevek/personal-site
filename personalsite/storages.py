import json
import os
from time import time

from storages.backends.s3 import S3Storage
import boto3
from botocore import exceptions
from urllib.request import urlopen, Request




class CustomS3Storage(S3Storage):

    bucket_name = "personal-bucket-058109276355-us-west-1-an"

    def __init__(self, **settings):
        super().__init__(**settings)

    def _save(self, name, content):
        try:
            return super()._save(name, content)
        except exceptions.ClientError as error:
            self.update_credentials()
            
        return super()._save(name, content)

    
    def update_credentials(self):
        req = Request(
            url="http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            method="PUT",
        )
        token = urlopen(req).read().decode()

        req = Request(
            url="http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance",
            headers={"X-aws-ec2-metadata-token": token},
        )
        res = json.loads(urlopen(req).read().decode())
       
        os.environ["AWS_ACCESS_KEY_ID"] = res["AccessKeyId"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = res["SecretAccessKey"]
