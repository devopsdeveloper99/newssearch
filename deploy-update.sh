#!/bin/bash -ex

cd /home/ec2-user/newssearch

# Stop any running Django app
pkill -f runserver || true

# Pull latest code
git pull origin main

# Ensure correct ownership
chown -R ec2-user:ec2-user /home/ec2-user/newssearch

# Activate virtual environment
source venv/bin/activate

# Install updated dependencies
pip install -r requirements.txt || true
pip install django requests 'urllib3<2.0' --force-reinstall

# OPTIONAL: Apply database migrations
# python manage.py migrate

# Run Django server in background and log output
nohup python3 manage.py runserver 0.0.0.0:8000 > /home/ec2-user/newssearch/server.log 2>&1 &
