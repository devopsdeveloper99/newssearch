#!/usr/bin/env python
"""
WSGI entry point for Django application.
This file tells the server to use Python/Passenger, not Node.js.
"""
import os
import sys

# Get the directory containing this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the project directory to the Python path
sys.path.insert(0, BASE_DIR)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
