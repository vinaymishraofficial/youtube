"""
WSGI config for youtube project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube.settings')

application = get_wsgi_application()

app = application

if __name__ == "__main__":
    from gunicorn.app.wsgiapp import run
    run()
