from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import os
import django
import websocket.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket.routing.websocket_urlpatterns)
    ),
})
