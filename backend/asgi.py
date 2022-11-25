"""
ASGI config for YoutubeScraper project.
It exposes the ASGI callable as a module-level variable named ``application``.
"""

# STDLIB LIBRARY
import os

# DJANGO LIBRARY
from django.core.asgi import get_asgi_application



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()
