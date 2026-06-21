import os
from django.core.wsgi import get_wsgi_application
"""
WSGI config for my_django_app project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application
# Set the default settings module for the 'wsgi' command.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproje.settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users.settings')
application = get_wsgi_application()
