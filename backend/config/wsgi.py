"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Added sys.path fix for Vercel
# Add the 'backend' directory to the Python path
path_root = Path(__file__).resolve().parent.parent.parent
if str(path_root / 'backend') not in sys.path:
    sys.path.append(str(path_root / 'backend'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
app = application
