import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from Platform import routings
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Platform.settings')
django.setup()


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': URLRouter(routings.websocket_urlpatterns),
})
