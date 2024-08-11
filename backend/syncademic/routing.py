from django.urls import re_path
from syncademic.consumers import NotificacionConsumidor

websocket_urlpatterns = [
    re_path(r'ws/notificaciones/', NotificacionConsumidor.as_asgi()),
    # Otras rutas WebSocket si es necesario
]
