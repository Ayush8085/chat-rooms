import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import rooms.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_rooms.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            rooms.routing.websocket_urlpatterns
        )
    )
})
