#!/usr/bin/env python
import os
import sys

import environ

if __name__ == '__main__':
    # This is to load the DJANGO_SETTINGS_MODULE from the .env file
    # The same code is used in project/wsgi.py
    root_dir = environ.Path(__file__) - 2
    env = environ.Env(DJANGO_SETTINGS_MODULE=(str, 'project.settings.production'))
    environ.Env.read_env(root_dir('.env'))

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
