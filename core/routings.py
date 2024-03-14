from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/play/(?P<room_name>\w+)/$', consumers.roomConsumer.as_asgi()),
]