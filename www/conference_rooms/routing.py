from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'device/', consumers.DeviceConsumer.as_asgi()),
]
