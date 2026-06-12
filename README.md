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
    listen       [::]:80;
    server_name  _ ;

    # Load configuration files for the default server block.
    include /etc/nginx/default.d/*.conf;

    location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
            alias /home/ec2-user/personal-site/static/;
    }

    error_page 404 /404.html;
    location = /404.html {
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
    }
}
. . .
```
9. Start it up!
```
sudo nginx
gunicorn personalsite.wsgi
```
