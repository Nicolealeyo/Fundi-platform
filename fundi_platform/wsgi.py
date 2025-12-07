"""
WSGI config for fundi_platform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application  # ✅ Correct import

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundi_platform.settings')

application = get_wsgi_application()  # ✅ Use WSGI here

