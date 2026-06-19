import json
import os
from time import time

from storages.backends.s3 import S3Storage
import boto3
from botocore import exceptions
from urllib.request import urlopen, Request




class CustomS3Storage(S3Storage):

    _last_updated = 0

    def __init__(self, **settings):
        _ = self.update_credentials()
        super().__init__(**settings)

    def _save(self, name, content):
        try:
            super()._save(name, content)
        except exceptions.ClientError as error:
            if error.response['Error']['Code'] == "InvalidAccessKeyId":
                self.update_credentials()
            else:
                raise error
            
        super()._save(name, content)

    
    def update_credentials(self):
        
        req = Request(
            url="http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            method="POST",
        )
        res = urlopen(req)
        token = res.read()

        req = Request(
            url="http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance",
            headers={"X-aws-ec2-metadata-token": token},
            method="GET",
        )
        res = json.loads(urlopen(req))

        os.environ["AWS_ACCESS_KEY_ID"] = res["AccessKeyId"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = res["SecretAccessKey"]

        self._last_updated = time()