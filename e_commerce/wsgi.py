"""
WSGI config for e_commerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/projects/Signup-Casuals/CommerceCore')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_commerce.settings')

application = get_wsgi_application()
