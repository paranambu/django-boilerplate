"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import environ

# This is to load the DJANGO_SETTINGS_MODULE from the .env file
# The same code is used in ../manage.py
root_dir = environ.Path(__file__) - 3
env = environ.Env(DJANGO_SETTINGS_MODULE=(str, 'project.settings.production'))
environ.Env.read_env(root_dir('.env'))

application = get_wsgi_application()
