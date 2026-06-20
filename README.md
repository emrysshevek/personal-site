# Deplyment steps:
1. If there is no ec2 instance running
    - setup instance with desired settings -- make sure to allow http and https from anywhere in security rules!!
    - Allocate elastic ip, associate with newly created instance
    - WAIT until instance is fully finished initializing. It takes a few minutes, just be patient
    - Connect to instance through preferred method
2. Install prerequisites
```
sudo dnf install git
sudo dnf install python3.12
sudo dnf install nginx
```
3. clone repository and navigate into repo
```
`git clone https://github.com/emrysshevek/personal-site.git`
cd personal-site
```
4. Set up environment
```
python3.12 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```
5. Migrate databases and collect static files
```
python manage.py migrate
python manage.py collectstatic
```
6. Modify Django settings file (personalsite/settings.py) for production. This prevents security vulnerabilies and prevents django from trying to serve static files itself
```
. . . 
DEBUG = False
. . . 
```
7. Modify nginx config file to act as proxy for our server
```
. . .
user ec2-user;
. . .
server {
    listen       80;
    listen       443 ssl http2;
    server_name  emrysshevek.com www.emrysshevek.com;
    large_client_header_buffers 4 32k;

    ssl_certificate         /etc/ssl/cert.pem;
    ssl_certificate_key     /etc/ssl/key.pem;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;
        proxy_pass http://localhost:8000;
    }

    location /static {
        alias /home/ec2-user/personal-site/static;
    }
}
. . .
```
8. Start it up!
```
sudo nginx
gunicorn personalsite.wsgi
```

# Setting up S3 connection
Django comes with a FileField (and ImageField subclass) along with the Storage class which make it fairly easy to save files/images to remote servers instead of the local filesystem. To hook it up to an Amazon S3 bucket, we first need to make a bucket, give our EC2 instance permissions to use the bucket, and make a custom Storage class that saves files to the bucket instead of the default behaviour. Even easier, we can use `django-storages` to do the heavy lifting of creating most of that custom storage class for us.

## Set up S3 Bucket
Under Amazon S3/Buckets go to 'Create Bucket'. Give your bucket a name (use Account Regional namespace if needed) and uncheck "Block all public access" to allow public access to the objects in the bucket. This is only necessary if you are planning to use the contents of the bucket as static files for your website (eg .js/.css files, images, etc).

## Create an EC2 Instance Role
Go to IAM/Roles and click "Create Role". 

For "trusted entity type" select AWS service and under the "Use Case" dropdown select EC2 as the service and use case. 

Give it the "AmazonS3FullAccess" permission.

## Modify EC2 Instance
Navigate to you EC2 instance and then go to Actions/Security/Modify IAM Role.

In the dropdown, select the Role you just created.

Back on the instance overview page, go to Actions/Instance Settings/Modify instance metadata options. Make sure 'Instance metadata service' is enabled, 'IMDSv2' is required, and set 'HTTP PUT response hop limit' to 2 (since we are using our nginx proxy).

## Modify Django Storage
Install django-storages for S3
```
pip install django-storages[s3]
```

Modify settings to allow django-storages //TODO FINISH SUMMARY

Normally we could just use django-storages as-is, but the id/key provided to our EC2 instance is changed about once an hour so we have to make sure our storage stays updated.
In a new file, create a class which inherits django-storages S3Storage
```(python)
import json
import os
from urllib.request import urlopen, Request

from storages.backends.s3 import S3Storage
from botocore import exceptions


class CustomS3Storage(S3Storage):

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
            method="GET",
        )
        res = json.loads(urlopen(req).read().decode())

        os.environ["AWS_ACCESS_KEY_ID"] = res["AccessKeyId"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = res["SecretAccessKey"]
```


