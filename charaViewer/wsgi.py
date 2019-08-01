"""
WSGI config for charaViewer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

VENV_SITE_DIRECTORY = os.environ.get("VENV_SITE_DIRECTORY", None)
if VENV_SITE_DIRECTORY is not None:
    sys.path.append(VENV_SITE_DIRECTORY)


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'charaViewer.settings')

application = get_wsgi_application()
