"""
WSGI config for charaViewer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

import sys

new_path = []
for path in sys.path:
    if 'venv' not in path:
        new_path.append(path)
sys.path = new_path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

try:
    from charaViewer.local_settings import VENV_SITE_DIRECTORY
    sys.path.append(VENV_SITE_DIRECTORY)
except ImportError:
    pass

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'charaViewer.settings')

application = get_wsgi_application()
