"""
ASGI config for project2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings') #確保在啟動時用正確的Django設定，它被設定為project2.settings

application = get_asgi_application()

# -----------------------------------------------------------
# asgi.py檔案的目的，是提供ASGI伺服器使用的「應用程式進入點」
