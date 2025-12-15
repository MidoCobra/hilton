# Deployment Checklist (Production)

This document outlines steps to deploy the `hilton` Django project in production using Gunicorn and Nginx on Ubuntu.

1. Prepare server (Ubuntu)

```bash
# update and install packages
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-venv python3-pip git nginx -y

# create a non-root user (optional) and a directory for the app
sudo useradd -m -s /bin/bash deployer
sudo passwd deployer
sudo mkdir -p /var/www/hilton
sudo chown deployer:deployer /var/www/hilton
```

2. Clone project & venv

```bash
cd /var/www/hilton
git clone https://github.com/MidoCobra/hilton.git .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create `.env` file

Copy `.env.example` into `.env` and update `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, database settings if needed.

4. Static and media

```bash
# create directories for media & staticfiles
mkdir -p /var/www/hilton/staticfiles
mkdir -p /var/www/hilton/media
chown -R deployer:deployer /var/www/hilton/staticfiles /var/www/hilton/media

# run collectstatic
python manage.py collectstatic --noinput
```

10. Generate site QR (optional)

```bash
# install the QR library (already listed in requirements)
pip install -r requirements.txt

# generate an SVG QR for your site and save to static/images/
python manage.py generate_qr --url https://ramseshilton.com

# the file will be at static/images/ramseshilton_qr.svg and can be included in templates
```

5. Configure Gunicorn

```bash
# run gunicorn (example)
gunicorn hilton_ramses.wsgi:application --bind 127.0.0.1:8000 --workers 3
```

6. Configure Nginx for static/media and reverse proxy
Create an nginx config referencing the `STATIC_ROOT` and `MEDIA_ROOT` (shown below in general structure):

```
server {
    listen 80;
    server_name yourdomain.com 165.227.144.15;

    location /static/ {
        alias /var/www/hilton/staticfiles/;
    }

    location /media/ {
        alias /var/www/hilton/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

7. Restart services

```bash
sudo systemctl restart nginx
# restart gunicorn or your systemd service
```

8. SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

9. Final checks

- Verify `DEBUG=False` in `.env`
- Ensure `ALLOWED_HOSTS` contains your domain & IP
- Run `python manage.py migrate` if needed
- Create superuser for admin
```

This file is a brief checklist; adjust details for your infrastructure.